import pandas as pd
import pytest

from src.data.preprocessing import clean_customer_data
from src.data.validation import validate_clean_data
from tests.test_preprocessing import make_raw_customer


def test_valid_data():
    df = clean_customer_data(make_raw_customer())

    validate_clean_data(df)


def test_duplicate_customer_ids():
    df = clean_customer_data(make_raw_customer())

    duplicated = pd.concat(
        [df, df],
        ignore_index=True,
    )

    with pytest.raises(ValueError, match="Duplicate"):
        validate_clean_data(duplicated)


def test_invalid_churn():
    df = clean_customer_data(make_raw_customer())

    df.loc[0, "churn"] = 2

    with pytest.raises(ValueError, match="churn"):
        validate_clean_data(df)


def test_negative_charges():
    df = clean_customer_data(make_raw_customer())

    df.loc[0, "monthly_charges"] = -10

    with pytest.raises(ValueError, match="Negative"):
        validate_clean_data(df)


def test_unexpected_missing_charges():
    raw = make_raw_customer()

    raw.loc[0, "tenure"] = "12"

    df = clean_customer_data(raw)

    with pytest.raises(ValueError, match="Missing"):
        validate_clean_data(df)
