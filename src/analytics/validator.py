import os


LOG_FILE = "outputs/ratio_edge_cases.log"


def log_edge_case(company, year, ratio_name, issue_type, details):
    """
    Log ratio anomalies to outputs/ratio_edge_cases.log
    """

    os.makedirs("outputs", exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"{company} | {year} | {ratio_name} | {issue_type} | {details}\n"
        )


def validate_ratio(value, ratio_name, company, year):
    """
    Validate computed ratio values.
    """

    if value is None:
        log_edge_case(
            company,
            year,
            ratio_name,
            "ZERO_DIVISION",
            "Returned None due to division by zero"
        )
        return None

    if value > 1000:
        log_edge_case(
            company,
            year,
            ratio_name,
            "EXTREME_RATIO",
            f"Value too high: {value}"
        )

    if value < -100:
        log_edge_case(
            company,
            year,
            ratio_name,
            "EXTREME_NEGATIVE",
            f"Value too low: {value}"
        )

    return value


def validate_equity(equity, company, year):
    """
    Check for negative or zero equity.
    """

    if equity is None:
        log_edge_case(
            company,
            year,
            "EQUITY",
            "MISSING_FIELD",
            "Equity value missing"
        )
        return False

    if equity <= 0:
        log_edge_case(
            company,
            year,
            "EQUITY",
            "NEGATIVE_BASE",
            f"Equity <= 0: {equity}"
        )
        return False

    return True


def validate_fields(data, required_fields, company, year):
    """
    Validate required fields exist in dataset row.
    """

    missing = []

    for field in required_fields:
        if field not in data or data[field] is None:
            missing.append(field)

    if missing:
        log_edge_case(
            company,
            year,
            "DATA",
            "MISSING_FIELD",
            f"Missing fields: {', '.join(missing)}"
        )
        return False

    return True