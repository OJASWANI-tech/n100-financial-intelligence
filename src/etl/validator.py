import pandas as pd
from src.etl.loader import load_all
import os

# Store all validation failures
validation_failures = []


# Log failure function
def log_failure(table, company_id, year, rule_id, severity, message):
    validation_failures.append({
        "table_name": table,
        "company_id": company_id,
        "year": year,
        "rule_id": rule_id,
        "severity": severity,
        "message": message
    })


# DQ-01: Primary Key uniqueness check
def check_company_pk(companies):
    duplicates = companies[companies["id"].duplicated()]

    for _, row in duplicates.iterrows():
        log_failure(
            "companies",
            row["id"],
            None,
            "DQ-01",
            "CRITICAL",
            "Duplicate company ID"
        )


# DQ-02: Composite PK uniqueness check
def check_composite_pk(df, table_name):
    if "company_id" in df.columns and "year" in df.columns:
        duplicates = df[df.duplicated(subset=["company_id", "year"])]

        for _, row in duplicates.iterrows():
            log_failure(
                table_name,
                row["company_id"],
                row["year"],
                "DQ-02",
                "CRITICAL",
                "Duplicate company_id-year combination"
            )

def check_fk(df, companies, table_name):
    valid_ids = set(companies["id"])

    for _, row in df.iterrows():
        if row["company_id"] not in valid_ids:
            log_failure(
                table_name,
                row["company_id"],
                row["year"],
                "DQ-03",
                "CRITICAL",
                "Foreign key violation"
            )
def check_balance_sheet(bs):
    for _, row in bs.iterrows():
        assets = row["total_assets"]
        liabilities = row["total_liabilities"]

        if pd.notnull(assets) and pd.notnull(liabilities):
            if abs(assets - liabilities) > (0.01 * assets):
                log_failure(
                    "balancesheet",
                    row["company_id"],
                    row["year"],
                    "DQ-04",
                    "WARNING",
                    "Balance sheet mismatch"
                )
def check_opm(pl):
    for _, row in pl.iterrows():
        sales = row["sales"]
        operating_profit = row["operating_profit"]
        opm = row["opm_percentage"]

        if pd.notnull(sales) and sales > 0:
            calc_opm = (operating_profit / sales) * 100

            if abs(calc_opm - opm) > 1:
                log_failure(
                    "profitandloss",
                    row["company_id"],
                    row["year"],
                    "DQ-05",
                    "WARNING",
                    "OPM mismatch"
                )
def check_sales(pl):
    for _, row in pl.iterrows():
        sales = row["sales"]

        if pd.notnull(sales):
            if sales <= 0:
                log_failure(
                    "profitandloss",
                    row["company_id"],
                    row["year"],
                    "DQ-06",
                    "CRITICAL",
                    "Sales must be positive"
                )  
# Main validator runner
def run_validations():
    data = load_all()

    # Run DQ-01
    check_company_pk(data["companies"])

    # Run DQ-02 only on relevant tables
    check_composite_pk(data["profitandloss"], "profitandloss")
    check_composite_pk(data["balancesheet"], "balancesheet")
    check_composite_pk(data["cashflow"], "cashflow")

    check_fk(data["profitandloss"], data["companies"], "profitandloss")
    check_fk(data["balancesheet"], data["companies"], "balancesheet")
    check_fk(data["cashflow"], data["companies"], "cashflow")

    check_balance_sheet(data["balancesheet"])
    check_opm(data["profitandloss"])
    check_sales(data["profitandloss"])

    # Create DataFrame
    df = pd.DataFrame(validation_failures)

    # Output file path
    output_path = "output/validation_failures.csv"

    # Remove old file if exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Save new validation report
    df.to_csv(output_path, index=False)

    print("Validation complete")
    print(f"Failures found: {len(df)}")


# Run file
if __name__ == "__main__":
    run_validations()