import pandas as pd

from src.data.preprocessing import clean_customer_data


def make_raw_customer() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customerID": ["TEST-001"],
            "gender": ["Female"],
            "SeniorCitizen": ["0"],
            "Partner": ["Yes"],
            "Dependents": ["No"],
            "tenure": ["0"],
            "PhoneService": ["Yes"],
            "MultipleLines": ["No"],
            "InternetService": ["DSL"],
            "OnlineSecurity": ["No"],
            "OnlineBackup": ["No"],
            "DeviceProtection": ["No"],
            "TechSupport": ["No"],
            "StreamingTV": ["No"],
            "StreamingMovies": ["No"],
            "Contract": ["Month-to-month"],
            "PaperlessBilling": ["Yes"],
            "PaymentMethod": ["Electronic check"],
            "MonthlyCharges": ["29.85"],
            "TotalCharges": [" "],
            "Churn": ["No"],
        }
    )


def test_column_renaming():
    result = clean_customer_data(make_raw_customer())

    assert "customer_id" in result.columns
    assert "customerID" not in result.columns


def test_missing_total_charges():
    result = clean_customer_data(make_raw_customer())

    assert result.loc[0, "total_charges"] == 0.0


def test_binary_conversion():
    result = clean_customer_data(make_raw_customer())

    assert result.loc[0, "partner"] == 1
    assert result.loc[0, "churn"] == 0


def test_numeric_conversion():
    result = clean_customer_data(make_raw_customer())

    assert result.loc[0, "monthly_charges"] == 29.85


def test_record_count_preserved():
    raw = make_raw_customer()

    result = clean_customer_data(raw)

    assert len(result) == len(raw)
