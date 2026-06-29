# tests/test_cashflow.py

from src.analytics.cashflow import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    classify_capital_allocation
)


def test_free_cash_flow_normal():
    assert free_cash_flow(500, -200) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(100, -300) == -200


def test_cfo_quality_high():
    cfo = [100, 120, 130, 140, 150]
    pat = [80, 100, 110, 120, 130]

    score, label = cfo_quality_score(cfo, pat)

    assert score > 1
    assert label == "High Quality"


def test_cfo_quality_moderate():
    cfo = [50, 60, 70, 80, 90]
    pat = [100, 100, 100, 100, 100]

    score, label = cfo_quality_score(cfo, pat)

    assert 0.5 <= score <= 1
    assert label == "Moderate"


def test_cfo_quality_accrual_risk():
    cfo = [10, 20, 30, 20, 10]
    pat = [100, 100, 100, 100, 100]

    score, label = cfo_quality_score(cfo, pat)

    assert score < 0.5
    assert label == "Accrual Risk"


def test_cfo_quality_pat_zero():
    cfo = [100, 120, 130, 140, 150]
    pat = [100, 0, 110, 120, 130]

    score, flag = cfo_quality_score(cfo, pat)

    assert score is None
    assert flag == "PAT_ZERO"


def test_capex_asset_light():
    capex, label = capex_intensity(-20, 1000)

    assert capex == 2.0
    assert label == "Asset Light"


def test_capex_capital_intensive():
    capex, label = capex_intensity(-200, 1000)

    assert capex == 20.0
    assert label == "Capital Intensive"


def test_fcf_conversion_zero_op():
    conversion, flag = fcf_conversion_rate(100, 0)

    assert conversion is None
    assert flag == "ZERO_OP"


def test_capital_allocation_reinvestor():
    pattern, label = classify_capital_allocation(
        500, -200, -100
    )

    assert pattern == ("+", "-", "-")
    assert label == "Reinvestor"


def test_capital_allocation_distress():
    pattern, label = classify_capital_allocation(
        -100, 50, 200
    )

    assert pattern == ("-", "+", "+")
    assert label == "Distress Signal"