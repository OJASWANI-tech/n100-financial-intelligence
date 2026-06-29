# src/analytics/cashflow.py


def free_cash_flow(cfo, cfi):
    """
    Free Cash Flow (FCF)

    Formula:
    FCF = CFO + CFI

    Negative FCF is allowed.
    """
    return cfo + cfi


def cfo_quality_score(cfo_values, pat_values):
    """
    CFO Quality Score

    Formula:
    average(CFO / PAT) over 5 years

    Classification:
    >1.0 = High Quality
    0.5 - 1.0 = Moderate
    <0.5 = Accrual Risk
    """

    if len(cfo_values) < 5 or len(pat_values) < 5:
        return None, "INSUFFICIENT"

    ratios = []

    for cfo, pat in zip(cfo_values[-5:], pat_values[-5:]):
        if pat == 0:
            return None, "PAT_ZERO"

        ratios.append(cfo / pat)

    avg_ratio = round(sum(ratios) / len(ratios), 2)

    if avg_ratio > 1.0:
        label = "High Quality"
    elif avg_ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return avg_ratio, label


def capex_intensity(cfi, sales):
    """
    CapEx Intensity

    Formula:
    abs(CFI) / sales * 100

    Classification:
    <3% = Asset Light
    3-8% = Moderate
    >8% = Capital Intensive
    """

    if sales == 0:
        return None, "ZERO_SALES"

    capex = round((abs(cfi) / sales) * 100, 2)

    if capex < 3:
        label = "Asset Light"
    elif capex <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return capex, label


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate

    Formula:
    FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None, "ZERO_OP"

    conversion = round((fcf / operating_profit) * 100, 2)

    return conversion, None


def get_sign(value):
    """
    Convert value into sign (+/-)
    """

    if value >= 0:
        return "+"
    return "-"


def classify_capital_allocation(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Capital Allocation Pattern Classifier
    """

    cfo_sign = get_sign(cfo)
    cfi_sign = get_sign(cfi)
    cff_sign = get_sign(cff)

    pattern = (cfo_sign, cfi_sign, cff_sign)

    # (+,-,-)
    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            return pattern, "Shareholder Returns"
        return pattern, "Reinvestor"

    # (+,+,-)
    elif pattern == ("+", "+", "-"):
        return pattern, "Liquidating Assets"

    # (-,+,+)
    elif pattern == ("-", "+", "+"):
        return pattern, "Distress Signal"

    # (-,-,+)
    elif pattern == ("-", "-", "+"):
        return pattern, "Growth Funded by Debt"

    # (+,+,+)
    elif pattern == ("+", "+", "+"):
        return pattern, "Cash Accumulator"

    # (-,-,-)
    elif pattern == ("-", "-", "-"):
        return pattern, "Pre-Revenue"

    # (+,-,+)
    elif pattern == ("+", "-", "+"):
        return pattern, "Mixed"

    else:
        return pattern, "Unclassified"


def compute_cashflow_metrics(
    cfo,
    cfi,
    cff,
    sales,
    pat_values,
    cfo_values,
    operating_profit
):
    """
    Compute all cashflow KPIs together
    """

    fcf = free_cash_flow(cfo, cfi)

    cfo_quality, cfo_quality_label = cfo_quality_score(
        cfo_values,
        pat_values
    )

    capex, capex_label = capex_intensity(cfi, sales)

    fcf_conversion, fcf_flag = fcf_conversion_rate(
        fcf,
        operating_profit
    )

    capital_pattern, pattern_label = classify_capital_allocation(
        cfo,
        cfi,
        cff,
        cfo_quality
    )

    return {
        "free_cash_flow": fcf,

        "cfo_quality_score": cfo_quality,
        "cfo_quality_label": cfo_quality_label,

        "capex_intensity": capex,
        "capex_label": capex_label,

        "fcf_conversion_rate": fcf_conversion,
        "fcf_conversion_flag": fcf_flag,

        "cfo_sign": capital_pattern[0],
        "cfi_sign": capital_pattern[1],
        "cff_sign": capital_pattern[2],
        "pattern_label": pattern_label,
    }