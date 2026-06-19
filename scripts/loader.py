import sqlite3
import pandas as pd
import os

# Connect database
conn = sqlite3.connect("database/n100.db")
conn.execute("PRAGMA foreign_keys = ON")

# Raw data folder
RAW_DATA_PATH = "data/raw"

# File-to-table mapping
files = {
    "companies.xlsx": "companies",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
    "financial_ratios.xlsx": "financial_ratios",
    "balancesheet.xlsx": "balance_sheet",
    "profitandloss.xlsx": "profit_loss",
    "cashflow.xlsx": "cash_flow",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "documents.xlsx": "documents",
    "analysis.xlsx": "analysis",
    "prosandcons.xlsx": "pros_cons"
}

for file_name, table_name in files.items():
    file_path = os.path.join(RAW_DATA_PATH, file_name)

    if os.path.exists(file_path):
        print(f"\nLoading {file_name} into {table_name}...")

        try:
            # Skip first title row
            df = pd.read_excel(file_path, skiprows=1)

            # Clean column names
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.replace("-", "_")
                .str.replace("/", "_")
            )

            # Drop fully empty rows
            df.dropna(how="all", inplace=True)

            # Remove duplicate rows
            df.drop_duplicates(inplace=True)

            print("Columns found:", list(df.columns))

            # Insert into SQLite
            df.to_sql(table_name, conn, if_exists="append", index=False)

            print(f"{table_name} loaded successfully.")

        except Exception as e:
            print(f"Error loading {file_name}: {e}")

    else:
        print(f"{file_name} not found.")

conn.commit()
conn.close()

print("\nAll datasets processed.")