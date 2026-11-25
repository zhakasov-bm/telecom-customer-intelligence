import pandas as pd

COLUMN_MAPPING = {
    "customerID": "customer_id",
    "gender": "gender",
    "SeniorCitizen": "senior_citizen",
    "Partner": "partner",
    "Dependents": "dependents",
    "tenure": "tenure",
    "PhoneService": "phone_service",
    "MultipleLines": "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity": "online_security",
    "OnlineBackup": "online_backup",
    "DeviceProtection": "device_protection",
    "TechSupport": "tech_support",
    "StreamingTV": "streaming_tv",
    "StreamingMovies": "streaming_movies",
    "Contract": "contract",
    "PaperlessBilling": "paperless_billing",
    "PaymentMethod": "payment_method",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
    "Churn": "churn",
}


def clean_customer_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Transform raw telecom data into a clean dataset."""

    df = df.copy()

    # Standardize column names
    df = df.rename(columns=COLUMN_MAPPING)

    # Remove leading and trailing whitespace
    string_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in string_columns:
        df[column] = df[column].str.strip()

    # Replace empty strings with missing values
    df = df.replace("", pd.NA)

    # Convert numeric columns
    numeric_columns = [
        "tenure",
        "senior_citizen",
        "monthly_charges",
        "total_charges",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="raise",
        )

    # Handle missing charges for new customers
    new_customer_mask = df["total_charges"].isna() & df["tenure"].eq(0)

    df.loc[
        new_customer_mask,
        "total_charges",
    ] = 0.0

    # Convert binary columns
    binary_columns = [
        "partner",
        "dependents",
        "phone_service",
        "paperless_billing",
        "churn",
    ]

    for column in binary_columns:
        df[column] = df[column].map({"Yes": 1, "No": 0})

    # Set explicit numeric data types
    integer_columns = [
        "tenure",
        "senior_citizen",
        *binary_columns,
    ]

    df[integer_columns] = df[integer_columns].astype("Int64")

    df["monthly_charges"] = df["monthly_charges"].astype("float64")

    df["total_charges"] = df["total_charges"].astype("float64")

    return df
