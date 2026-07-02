import os
from src.analytics.validator import (
    validate_ratio,
    validate_equity,
    validate_fields
)


LOG_FILE = "outputs/ratio_edge_cases.log"


def setup_module():
    """
    Clear log file before tests.
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def test_zero_division():
    result = validate_ratio(
        None,
        "ROE",
        "TCS",
        2025
    )
    assert result is None


def test_extreme_ratio():
    result = validate_ratio(
        1500,
        "ROCE",
        "INFY",
        2024
    )
    assert result == 1500


def test_negative_ratio():
    result = validate_ratio(
        -200,
        "ROE",
        "WIPRO",
        2023
    )
    assert result == -200


def test_negative_equity():
    result = validate_equity(
        -500,
        "RELIANCE",
        2025
    )
    assert result is False


def test_valid_equity():
    result = validate_equity(
        1000,
        "HDFC",
        2025
    )
    assert result is True


def test_missing_fields():
    data = {
        "sales": 1000,
        "profit": None
    }

    required_fields = ["sales", "profit", "equity"]

    result = validate_fields(
        data,
        required_fields,
        "TATASTEEL",
        2025
    )

    assert result is False


def test_valid_fields():
    data = {
        "sales": 1000,
        "profit": 100,
        "equity": 500
    }

    required_fields = ["sales", "profit", "equity"]

    result = validate_fields(
        data,
        required_fields,
        "ITC",
        2025
    )

    assert result is True