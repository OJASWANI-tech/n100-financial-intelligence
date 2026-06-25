
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


# DQ-01: Primary Key uniqueness
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


# DQ-02: Composite PK uniqueness
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


# DQ-03: Foreign key integrity (optimized)
def check_fk(df, companies, table_name):
    valid_ids = set(companies["id"])

    invalid_rows = df[~df["company_id"].isin(valid_ids)]

    for _, row in invalid_rows.iterrows():
        log_failure(
            table_name,
            row["company_id"],
            row["year"],
            "DQ-03",
            "CRITICAL",
            "Foreign key violation"
        )


# DQ-04: Balance sheet check
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


# DQ-05: OPM cross-check
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


# DQ-06: Positive sales
def check_sales(pl):
    for _, row in pl.iterrows():
        sales = row["sales"]

        if pd.notnull(sales) and sales <= 0:
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
    global validation_failures
    validation_failures = []

    print("Loading data...")
    data = load_all()

    print("Running DQ-01...")
    check_company_pk(data["companies"])

    print("Running DQ-02...")
    check_composite_pk(data["profitandloss"], "profitandloss")
    check_composite_pk(data["balancesheet"], "balancesheet")
    check_composite_pk(data["cashflow"], "cashflow")

    print("Running DQ-03...")
    check_fk(data["profitandloss"], data["companies"], "profitandloss")
    check_fk(data["balancesheet"], data["companies"], "balancesheet")
    check_fk(data["cashflow"], data["companies"], "cashflow")

    print("Running DQ-04...")
    check_balance_sheet(data["balancesheet"])

    print("Running DQ-05...")
    check_opm(data["profitandloss"])

    print("Running DQ-06...")
    check_sales(data["profitandloss"])

    # Create validation report
    df = pd.DataFrame(validation_failures)

    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/validation_failures.csv"

    df.to_csv(output_path, index=False)

    print("\nValidation complete")
    print(f"Failures found: {len(df)}")
    print(f"Saved to: {output_path}")


# Run validator
if __name__ == "__main__":
    run_validations()
