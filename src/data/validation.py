import pandas as pd

from src.data.preprocessing import COLUMN_MAPPING


def validate_clean_data(
    df: pd.DataFrame,
) -> None:
    """Validate the transformed customer dataset."""

    expected_columns = set(COLUMN_MAPPING.values())

    missing_columns = expected_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset is empty")

    if df.isna().any().any():
        missing = df.isna().sum()
        missing = missing[missing > 0]

        raise ValueError(f"Missing values detected:\n{missing}")

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs")

    if df["customer_id"].str.strip().eq("").any():
        raise ValueError("Empty customer IDs")

    if not df["tenure"].between(0, 72).all():
        raise ValueError("Invalid tenure values")

    if (df["monthly_charges"] < 0).any():
        raise ValueError("Negative monthly charges")

    if (df["total_charges"] < 0).any():
        raise ValueError("Negative total charges")

    binary_columns = [
        "senior_citizen",
        "partner",
        "dependents",
        "phone_service",
        "paperless_billing",
        "churn",
    ]

    for column in binary_columns:
        if not df[column].isin([0, 1]).all():
            raise ValueError(f"Invalid binary values in {column}")
