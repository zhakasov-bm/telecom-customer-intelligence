import logging

import pandas as pd
from sqlalchemy import text

from src.config import RAW_DATA_PATH, engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def extract_data() -> pd.DataFrame:
    """Read the raw telecom dataset."""

    logger.info("Reading dataset: %s", RAW_DATA_PATH)

    df = pd.read_csv(
        RAW_DATA_PATH,
        dtype=str,
        keep_default_na=False,
    )

    logger.info(
        "Dataset loaded: %s rows, %s columns",
        df.shape[0],
        df.shape[1],
    )

    return df


def validate_data(df: pd.DataFrame) -> None:
    """Perform basic dataset validation."""

    required_columns = {
        "customerID",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset is empty")

    if df["customerID"].str.strip().eq("").any():
        raise ValueError("Empty customer IDs detected")

    if df["customerID"].duplicated().any():
        raise ValueError("Duplicate customer IDs detected")

    if not df["Churn"].isin(["Yes", "No"]).all():
        raise ValueError("Invalid Churn values detected")

    logger.info("Data validation passed")


def load_data(df: pd.DataFrame) -> None:
    """Load raw customer data into PostgreSQL."""

    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

        df.to_sql(
            name="customers",
            con=connection,
            schema="raw",
            if_exists="replace",
            index=False,
            chunksize=1000,
        )

    logger.info(
        "Successfully loaded %s records into raw.customers",
        len(df),
    )


def run_pipeline() -> None:

    logger.info("Starting ingestion pipeline")

    df = extract_data()

    validate_data(df)

    load_data(df)

    logger.info("Ingestion pipeline completed")


if __name__ == "__main__":
    run_pipeline()
