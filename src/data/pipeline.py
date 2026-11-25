import logging

import pandas as pd
from sqlalchemy import BigInteger, Float, Text, text

from src.config import BASE_DIR, engine
from src.data.preprocessing import clean_customer_data
from src.data.validation import validate_clean_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def extract() -> pd.DataFrame:
    """Extract customer data from the raw layer."""

    logger.info("Extracting raw customer data")

    return pd.read_sql(
        "SELECT * FROM raw.customers",
        engine,
    )


def transform(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Clean and validate customer data."""

    logger.info("Transforming customer data")

    cleaned_df = clean_customer_data(df)

    validate_clean_data(cleaned_df)

    if len(cleaned_df) != len(df):
        raise ValueError("Unexpected record loss during transformation")

    logger.info("Data validation passed")

    return cleaned_df


def load(df: pd.DataFrame) -> None:
    """Load cleaned data and refresh analytics views."""

    logger.info("Loading staging data")

    sql_path = BASE_DIR / "sql" / "02_analytics_views.sql"

    analytics_sql = sql_path.read_text(encoding="utf-8")

    column_types = {}

    for column in df.columns:
        if pd.api.types.is_integer_dtype(df[column]):
            column_types[column] = BigInteger()
        elif pd.api.types.is_float_dtype(df[column]):
            column_types[column] = Float()
        else:
            column_types[column] = Text()

    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))

        # Drop dependent views before replacing the table
        for view in [
            "customer_overview",
            "churn_by_contract",
            "churn_by_internet",
        ]:
            connection.execute(text(f"DROP VIEW IF EXISTS analytics.{view}"))

        df.to_sql(
            name="customers",
            con=connection,
            schema="staging",
            if_exists="replace",
            index=False,
            chunksize=1000,
            dtype=column_types,
        )

        connection.execute(
            text(
                """
                ALTER TABLE staging.customers
                ADD PRIMARY KEY (customer_id)
                """
            )
        )

        # Recreate analytics views
        for statement in analytics_sql.split(";"):
            if statement.strip():
                connection.execute(text(statement))

    logger.info(
        "Loaded %s customers into staging.customers",
        len(df),
    )


def run_pipeline() -> None:
    logger.info("Starting ETL pipeline")

    raw_df = extract()

    cleaned_df = transform(raw_df)

    load(cleaned_df)

    logger.info("ETL pipeline completed")


if __name__ == "__main__":
    run_pipeline()
