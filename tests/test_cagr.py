from src.analytics.cagr import (
    calculate_cagr,
    get_window_values,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)


# Test normal CAGR calculation
def test_calculate_cagr_normal():
    value, flag = calculate_cagr(100, 200, 3)

    assert value is not None
    assert flag is None


# Test zero base
def test_calculate_cagr_zero_base():
    value, flag = calculate_cagr(0, 200, 3)

    assert value is None
    assert flag == "ZERO_BASE"


# Test positive to negative
def test_calculate_cagr_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 3)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


# Test negative to positive
def test_calculate_cagr_turnaround():
    value, flag = calculate_cagr(-50, 100, 3)

    assert value is None
    assert flag == "TURNAROUND"


# Test negative to negative
def test_calculate_cagr_both_negative():
    value, flag = calculate_cagr(-100, -50, 3)

    assert value is None
    assert flag == "BOTH_NEGATIVE"


# Test insufficient data
def test_get_window_values_insufficient():
    start, end, flag = get_window_values([100, 200], 5)

    assert start is None
    assert end is None
    assert flag == "INSUFFICIENT"


# Test get window values normal
def test_get_window_values_normal():
    start, end, flag = get_window_values([100, 120, 150, 200], 3)

    assert start == 120
    assert end == 200
    assert flag is None


# Test revenue CAGR
def test_revenue_cagr():
    revenues = [100, 120, 150, 180, 250]

    result = revenue_cagr(revenues)

    assert "3Y" in result
    assert "5Y" in result
    assert "10Y" in result
    assert result["10Y"][1] == "INSUFFICIENT"


# Test PAT CAGR
def test_pat_cagr():
    pats = [10, 12, 15, 20, 30]

    result = pat_cagr(pats)

    assert result["3Y"][0] is not None


# Test EPS CAGR
def test_eps_cagr():
    eps = [2, 3, 4, 5, 8]

    result = eps_cagr(eps)

    assert result["3Y"][0] is not None