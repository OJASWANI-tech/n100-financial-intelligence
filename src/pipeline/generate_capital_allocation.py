# src/pipeline/generate_capital_allocation.py

import sqlite3
import pandas as pd

from src.analytics.cashflow import compute_cashflow_metrics


def generate_capital_allocation():
    """
    Generate capital_allocation.csv from SQLite database
    """

    # Connect to the REAL database
    conn = sqlite3.connect("database/n100.db")

    # Join cash_flow + profit_loss tables
    query = """
    SELECT
        cf.company_id,
        cf.year,
        cf.operating_activity,
        cf.investing_activity,
        cf.financing_activity,
        pl.sales,
        pl.net_profit,
        pl.operating_profit
    FROM cash_flow cf
    JOIN profit_loss pl
        ON cf.company_id = pl.company_id
        AND cf.year = pl.year
    ORDER BY cf.company_id, cf.year
    """

    df = pd.read_sql(query, conn)

    rows = []

    # Loop company-wise
    for company_id in df["company_id"].unique():

        company_df = df[df["company_id"] == company_id].sort_values("year")

        cfo_values = company_df["operating_activity"].tolist()
        pat_values = company_df["net_profit"].tolist()

        for _, row in company_df.iterrows():

            metrics = compute_cashflow_metrics(
                cfo=row["operating_activity"],
                cfi=row["investing_activity"],
                cff=row["financing_activity"],
                sales=row["sales"],
                pat_values=pat_values,
                cfo_values=cfo_values,
                operating_profit=row["operating_profit"]
            )

            rows.append({
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign": metrics["cfo_sign"],
                "cfi_sign": metrics["cfi_sign"],
                "cff_sign": metrics["cff_sign"],
                "pattern_label": metrics["pattern_label"]
            })

    # Create final CSV
    output_df = pd.DataFrame(rows)

    output_df.to_csv(
        "outputs/capital_allocation.csv",
        index=False
    )

    conn.close()

    print("Capital allocation file saved: outputs/capital_allocation.csv")


if __name__ == "__main__":
    generate_capital_allocation()