from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    roe,
    roce,
    roa,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover
)


# -------------------------
# DAY 8 — PROFITABILITY
# -------------------------

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


# -------------------------
# DAY 9 — LEVERAGE & EFFICIENCY
# -------------------------

# Test 9 — Debt-free returns 0
def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 50) == 0


# Test 10 — Normal D/E
def test_debt_to_equity():
    assert debt_to_equity(300, 100, 50) == 2


# Test 11 — High leverage flag
def test_high_leverage_flag():
    assert high_leverage_flag(6, "Metals") is True


# Test 12 — Financial sector exemption
def test_high_leverage_financials():
    assert high_leverage_flag(8, "Financials") is False


# Test 13 — ICR interest zero
def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(100, 20, 0) is None


# Test 14 — ICR label debt free
def test_icr_label():
    assert icr_label(None) == "Debt Free"


# Test 15 — ICR warning
def test_icr_warning_flag():
    assert icr_warning_flag(1.2) is True


# Test 16 — Net debt
def test_net_debt():
    assert net_debt(500, 200) == 300


# Test 17 — Asset turnover zero assets
def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None


# Test 18 — Asset turnover normal
def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2