
import sqlite3
import pandas as pd
import os
import traceback

# Connect database
conn = sqlite3.connect("database/n100.db")
conn.execute("PRAGMA foreign_keys = ON")

# Clear old data before reload
tables_to_clear = [
    "pros_cons",
    "analysis",
    "documents",
    "peer_groups",
    "market_cap",
    "stock_prices",
    "cash_flow",
    "profit_loss",
    "balance_sheet",
    "financial_ratios",
    "sectors",
    "companies"
]

for table in tables_to_clear:
    conn.execute(f"DELETE FROM {table}")

conn.commit()
print("Old data cleared.\n")

RAW_DATA_PATH = "data/raw"
OUTPUT_PATH = "outputs"

os.makedirs(OUTPUT_PATH, exist_ok=True)

# Files that DO NOT need skiprows=1
special_skip_0 = [
    "sectors.xlsx",
    "financial_ratios.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx"
]

# Proper load order (Parent → Child)
files = [
    ("companies.xlsx", "companies"),
    ("sectors.xlsx", "sectors"),
    ("financial_ratios.xlsx", "financial_ratios"),
    ("balancesheet.xlsx", "balance_sheet"),
    ("profitandloss.xlsx", "profit_loss"),
    ("cashflow.xlsx", "cash_flow"),
    ("stock_prices.xlsx", "stock_prices"),
    ("market_cap.xlsx", "market_cap"),
    ("peer_groups.xlsx", "peer_groups"),
    ("documents.xlsx", "documents"),
    ("analysis.xlsx", "analysis"),
    ("prosandcons.xlsx", "pros_cons")
]

audit_log = []

for file_name, table_name in files:
    file_path = os.path.join(RAW_DATA_PATH, file_name)

    if os.path.exists(file_path):
        print(f"\nLoading {file_name} → {table_name}")

        try:
            # Read Excel
            if file_name in special_skip_0:
                df = pd.read_excel(file_path)
            else:
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

            # Remove blank rows & duplicates
            df.dropna(how="all", inplace=True)
            df.drop_duplicates(inplace=True)

            # Clean company_id
            if "company_id" in df.columns:
                df["company_id"] = df["company_id"].astype(str).str.strip()

                df["company_id"] = df["company_id"].replace({
                     "AGTL": "ATGL"
                })
                valid_ids = pd.read_sql("SELECT id FROM companies", conn)["id"].tolist()
                df = df[df["company_id"].isin(valid_ids)]



            # Fix ID type
            if "id" in df.columns:
                if table_name == "companies":
                    # companies table uses TEXT ticker IDs
                    df["id"] = df["id"].astype(str).str.strip()
                else:
                    # child tables use INTEGER IDs
                    df["id"] = pd.to_numeric(df["id"], errors="coerce")

            # Get DB columns
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            db_columns = [row[1] for row in cursor.fetchall()]

            # Keep only matching columns
            df = df[[col for col in df.columns if col in db_columns]]

            # Debugging
            print("DB columns:", db_columns)
            print("DF columns:", df.columns.tolist())
            print("Rows:", len(df))

            # Count rows
            row_count = len(df)

            # Insert into DB
            df.to_sql(table_name, conn, if_exists="append", index=False)

            # Commit immediately
            conn.commit()

            audit_log.append({
                "file_name": file_name,
                "table_name": table_name,
                "rows_loaded": row_count,
                "status": "success"
            })

            print(f"{table_name} loaded ({row_count} rows)")

        except Exception as e:
            audit_log.append({
                "file_name": file_name,
                "table_name": table_name,
                "rows_loaded": 0,
                "status": f"failed: {repr(e)}"
            })

            print(f"\nFAILED FILE: {file_name}")
            traceback.print_exc()

    else:
        audit_log.append({
            "file_name": file_name,
            "table_name": table_name,
            "rows_loaded": 0,
            "status": "file not found"
        })

        print(f"{file_name} not found.")

# Save audit log
audit_df = pd.DataFrame(audit_log)
audit_df.to_csv(os.path.join(OUTPUT_PATH, "load_audit.csv"), index=False)

print("\nLoad audit saved → outputs/load_audit.csv")

# Row count verification
print("\nRow Count Verification:")
tables = [
    "companies",
    "profit_loss",
    "balance_sheet",
    "cash_flow",
    "stock_prices"
]

for table in tables:
    result = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn)
    print(f"{table}: {result['cnt'][0]}")

# Foreign key check
fk_check = pd.read_sql("PRAGMA foreign_key_check;", conn)

if fk_check.empty:
    print("\nFK Check: 0 issues found ✅")
else:
    print("\nFK Issues Found:")
    print(fk_check)

conn.close()

print("\nAll datasets processed successfully!")
