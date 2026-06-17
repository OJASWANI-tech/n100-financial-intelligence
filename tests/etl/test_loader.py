from src.etl.loader import load_excel


def test_load_companies():
    df = load_excel("companies.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_profit_loss():
    df = load_excel("profitandloss.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_balance_sheet():
    df = load_excel("balancesheet.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_cashflow():
    df = load_excel("cashflow.xlsx", header=1)
    assert df.shape[0] > 0

def test_load_analysis():
    df = load_excel("analysis.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_documents():
    df = load_excel("documents.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_prosandcons():
    df = load_excel("prosandcons.xlsx", header=1)
    assert df.shape[0] > 0


def test_load_sectors():
    df = load_excel("sectors.xlsx", header=0)
    assert df.shape[0] > 0


def test_load_stock_prices():
    df = load_excel("stock_prices.xlsx", header=0)
    assert df.shape[0] > 0


def test_load_market_cap():
    df = load_excel("market_cap.xlsx", header=0)
    assert df.shape[0] > 0


def test_load_financial_ratios():
    df = load_excel("financial_ratios.xlsx", header=0)
    assert df.shape[0] > 0


def test_load_peer_groups():
    df = load_excel("peer_groups.xlsx", header=0)
    assert df.shape[0] > 0