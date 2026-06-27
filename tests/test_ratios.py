from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    roe,
    roce,
    roa
)


# Test 1 — Net Profit Margin normal
def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20


# Test 2 — Net Profit Margin zero sales
def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None


# Test 3 — Operating Profit Margin normal
def test_operating_profit_margin():
    assert operating_profit_margin(150, 1000) == 15


# Test 4 — OPM mismatch
def test_opm_mismatch():
    result = operating_profit_margin(150, 1000, 10)
    assert result == 15


# Test 5 — ROE normal
def test_roe():
    assert roe(100, 200, 300) == 20


# Test 6 — ROE negative equity
def test_roe_negative_equity():
    assert roe(100, -200, 100) is None


# Test 7 — ROCE normal
def test_roce():
    assert roce(200, 300, 200, 500) == 20


# Test 8 — ROA zero assets
def test_roa_zero_assets():
    assert roa(100, 0) is None