from src.etl.normaliser import normalize_year, normalize_ticker


def test_normalize_ticker_1():
    assert normalize_ticker("tcs") == "TCS"


def test_normalize_ticker_2():
    assert normalize_ticker(" infy ") == "INFY"


def test_normalize_ticker_3():
    assert normalize_ticker("HDFCBANK") == "HDFCBANK"


def test_normalize_year_1():
    assert normalize_year("Mar-24") == "2024-03"


def test_normalize_year_2():
    assert normalize_year("Mar-23") == "2023-03"


def test_normalize_year_3():
    assert normalize_year("Dec-22") == "2022-12"

def test_normalize_ticker_4():
    assert normalize_ticker(" reliance ") == "RELIANCE"

def test_normalize_ticker_5():
    assert normalize_ticker(" hdfcbank") == "HDFCBANK"

def test_normalize_ticker_6():
    assert normalize_ticker("sbin ") == "SBIN"

def test_normalize_ticker_7():
    assert normalize_ticker("AxisBank") == "AXISBANK"

def test_normalize_ticker_8():
    assert normalize_ticker("") is None

def test_normalize_ticker_9():
    assert normalize_ticker(None) is None

def test_year_jan():
    assert normalize_year("Jan-20") == "2020-01"

def test_year_feb():
    assert normalize_year("Feb-21") == "2021-02"

def test_year_apr():
    assert normalize_year("Apr-22") == "2022-04"

def test_year_may():
    assert normalize_year("May-23") == "2023-05"

def test_year_jun():
    assert normalize_year("Jun-24") == "2024-06"

def test_year_jul():
    assert normalize_year("Jul-24") == "2024-07"

def test_year_aug():
    assert normalize_year("Aug-24") == "2024-08"

def test_year_sep():
    assert normalize_year("Sep-24") == "2024-09"

def test_year_oct():
    assert normalize_year("Oct-24") == "2024-10"

def test_year_nov():
    assert normalize_year("Nov-24") == "2024-11"

def test_year_dec():
    assert normalize_year("Dec-24") == "2024-12"