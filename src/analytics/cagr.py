# src/analytics/cagr.py


def calculate_cagr(start, end, years):
    """
    Generic CAGR calculator

    Formula:
    CAGR = ((end / start) ** (1 / years) - 1) * 100

    Returns:
        tuple: (cagr_value, flag)
    """

    # Edge Case 1: Invalid years
    if years <= 0:
        return None, "INSUFFICIENT"

    # Edge Case 2: Zero base
    if start == 0:
        return None, "ZERO_BASE"

    # Edge Case 3: Positive -> Negative
    if start > 0 and end < 0:
        return None, "DECLINE_TO_LOSS"

    # Edge Case 4: Negative -> Positive
    if start < 0 and end > 0:
        return None, "TURNAROUND"

    # Edge Case 5: Negative -> Negative
    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    # Normal Case
    cagr = ((end / start) ** (1 / years) - 1) * 100

    return round(cagr, 2), None


def get_window_values(values, window):
    """
    Extract start and end values for CAGR window

    Example:
        values = [100, 120, 140, 170, 220]
        window = 3

        start = 140
        end = 220
    """

    if len(values) < window:
        return None, None, "INSUFFICIENT"

    start = values[-window]
    end = values[-1]

    return start, end, None


def revenue_cagr(revenues):
    """
    Compute Revenue CAGR for 3Y, 5Y, 10Y
    """

    result = {}

    for years in [3, 5, 10]:
        start, end, flag = get_window_values(revenues, years)

        if flag:
            result[f"{years}Y"] = (None, flag)
            continue

        result[f"{years}Y"] = calculate_cagr(start, end, years)

    return result


def pat_cagr(pats):
    """
    Compute PAT CAGR for 3Y, 5Y, 10Y
    """

    result = {}

    for years in [3, 5, 10]:
        start, end, flag = get_window_values(pats, years)

        if flag:
            result[f"{years}Y"] = (None, flag)
            continue

        result[f"{years}Y"] = calculate_cagr(start, end, years)

    return result


def eps_cagr(eps_values):
    """
    Compute EPS CAGR for 3Y, 5Y, 10Y
    """

    result = {}

    for years in [3, 5, 10]:
        start, end, flag = get_window_values(eps_values, years)

        if flag:
            result[f"{years}Y"] = (None, flag)
            continue

        result[f"{years}Y"] = calculate_cagr(start, end, years)

    return result