#loads data
import os
import pandas as pd
from src.etl.normaliser import normalize_year, normalize_ticker

DATA_PATH = "data/raw"

FILES = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "market_cap": "market_cap.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx"
}


def load_excel(file_name, header=0):
    path = os.path.join(DATA_PATH, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_name} not found!")

    df = pd.read_excel(path, header=header)
    return df


def process_dataframe(df):
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)

    return df


def load_all():
    loaded_data = {}

    for name, file in FILES.items():
        header = 1 if name in [
            "companies",
            "profitandloss",
            "balancesheet",
            "cashflow",
            "analysis",
            "documents",
            "prosandcons"
        ] else 0

        print(f"Loading {file}...")
        df = load_excel(file, header)
        df = process_dataframe(df)
        loaded_data[name] = df

        print(f"{name}: {df.shape}")

    return loaded_data


if __name__ == "__main__":
    data = load_all()
    print("All datasets loaded successfully.")