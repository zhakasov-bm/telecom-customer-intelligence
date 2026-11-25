import pandas as pd

from src.config import engine


def load_raw_data() -> pd.DataFrame:
    """Load raw customer data from PostgreSQL."""

    return pd.read_sql(
        "SELECT * FROM raw.customers",
        engine,
    )


def profile_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a column-level data quality report."""

    report = pd.DataFrame(
        {
            "data_type": df.dtypes.astype(str),
            "missing_values": df.isna().sum(),
            "empty_strings": df.apply(
                lambda col: col.astype(str).str.strip().eq("").sum()
            ),
            "unique_values": df.nunique(),
            "missing_percentage": (df.isna().mean() * 100).round(2),
        }
    )

    return report


def main() -> None:
    df = load_raw_data()

    print("\nDATASET OVERVIEW")
    print("=" * 60)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("\nCOLUMN PROFILE")
    print("=" * 60)

    print(profile_data(df).to_string())

    print("\nTARGET DISTRIBUTION")
    print("=" * 60)

    print(df["Churn"].value_counts())

    print("\nEMPTY TOTAL CHARGES")
    print("=" * 60)

    print(
        df.loc[
            df["TotalCharges"].str.strip().eq(""),
            ["customerID", "tenure", "TotalCharges"],
        ]
    )


if __name__ == "__main__":
    main()
