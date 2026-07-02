import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Step 3 — Net Profit Margin
def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None
    return (net_profit / sales) * 100


# Step 4 — Operating Profit Margin
def operating_profit_margin(operating_profit, sales, opm_percentage=None):
    if sales == 0:
        return None

    calculated_opm = (operating_profit / sales) * 100

    if opm_percentage is not None:
        if abs(calculated_opm - opm_percentage) > 1:
            logger.warning(
                f"OPM mismatch: Calculated={calculated_opm}, Reported={opm_percentage}"
            )

    return calculated_opm


# Step 5 — ROE
def roe(net_profit, equity_capital, reserves):
    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100


# Step 6 — ROCE
def roce(ebit, equity_capital, reserves, borrowings):
    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


# Financial sector checker (placeholder)
def is_financial_company(broad_sector):
    return broad_sector.lower() == "financials"


# Step 7 — ROA
def roa(net_profit, total_assets):
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100
# -------------------------
# DAY 9 — LEVERAGE RATIOS
# -------------------------

def debt_to_equity(borrowings, equity_capital, reserves):
    total_equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if total_equity == 0:
        return None

    return borrowings / total_equity


def high_leverage_flag(de_ratio, sector):
    return de_ratio > 5 and sector != "Financials"


def interest_coverage_ratio(operating_profit, other_income, interest):
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(icr):
    if icr is None:
        return "Debt Free"
    return None


def icr_warning_flag(icr):
    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    return borrowings - investments


# -------------------------
# DAY 9 — EFFICIENCY RATIOS
# -------------------------

def asset_turnover(sales, total_assets):
    if total_assets == 0:
        return None

    return sales / total_assets

def interest_coverage(operating_profit, interest):
    if interest == 0:
        return None
    return round(operating_profit / interest, 2)


def asset_turnover(sales, total_assets):
    if total_assets == 0:
        return None
    return round(sales / total_assets, 2)


def debt_to_equity(total_debt, equity):
    if equity == 0:
        return None
    return round(total_debt / equity, 2)
def earnings_per_share(net_profit, shares_outstanding):
    if shares_outstanding == 0:
        return None
    return round(net_profit / shares_outstanding, 2)
def book_value_per_share(equity_capital, reserves, shares_outstanding):
    if shares_outstanding == 0:
        return None
    return round((equity_capital + reserves) / shares_outstanding, 2)
def dividend_payout_ratio(dividend_paid, net_profit):
    if net_profit == 0:
        return None
    return round((dividend_paid / net_profit) * 100, 2)