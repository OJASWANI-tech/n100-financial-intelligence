#it cleans data 
import re


def normalize_year(year):
    """
    Convert formats like:
    Mar-24 -> 2024-03
    Mar-23 -> 2023-03
    """
    if isinstance(year, str):
        match = re.match(r"([A-Za-z]+)-(\d{2})", year.strip())
        if match:
            month, yy = match.groups()
            full_year = int("20" + yy)
            month_map = {
                "Jan": "01", "Feb": "02", "Mar": "03",
                "Apr": "04", "May": "05", "Jun": "06",
                "Jul": "07", "Aug": "08", "Sep": "09",
                "Oct": "10", "Nov": "11", "Dec": "12"
            }
            return f"{full_year}-{month_map.get(month[:3], '01')}"
    return None


def normalize_ticker(ticker):
    """
    Clean ticker names:
    tcs -> TCS
    infy  -> INFY
    """
    if ticker:
        return str(ticker).strip().upper()
    return None