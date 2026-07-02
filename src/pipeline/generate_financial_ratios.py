import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    roe,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
    earnings_per_share,
    book_value_per_share,
    dividend_payout_ratio
)

from src.analytics.cagr import calculate_cagr
from src.analytics.cashflow import free_cash_flow
from src.analytics.validator import validate_ratio


DB_PATH = "database/n100.db"


def generate_financial_ratios():
    conn = sqlite3.connect(DB_PATH)

    profit_loss = pd.read_sql(
        "SELECT * FROM profit_loss", conn
    ).sort_values(["company_id", "year"]).reset_index(drop=True)

    balance_sheet = pd.read_sql(
        "SELECT * FROM balance_sheet", conn
    ).sort_values(["company_id", "year"]).reset_index(drop=True)

    cash_flow = pd.read_sql(
        "SELECT * FROM cash_flow", conn
    ).sort_values(["company_id", "year"]).reset_index(drop=True)

    records = []

    company_ids = profit_loss["company_id"].unique()

    for company in company_ids:

        company_pl = profit_loss[
            profit_loss["company_id"] == company
        ].reset_index(drop=True)

        company_bs = balance_sheet[
            balance_sheet["company_id"] == company
        ].reset_index(drop=True)

        company_cf = cash_flow[
            cash_flow["company_id"] == company
        ].reset_index(drop=True)

        for i in range(len(company_pl)):

            if i >= len(company_bs) or i >= len(company_cf):
                continue

            pl_row = company_pl.iloc[i]
            bs_row = company_bs.iloc[i]
            cf_row = company_cf.iloc[i]

            year = pl_row["year"]

            # Profit & Loss
            sales = pl_row.get("sales", 0)
            net_profit = pl_row.get("net_profit", 0)
            operating_profit = pl_row.get("operating_profit", 0)
            interest = pl_row.get("interest", 0)

            # Balance Sheet
            equity_capital = bs_row.get("equity_capital", 0)
            reserves = bs_row.get("reserves", 0)
            equity = equity_capital + reserves
            debt = bs_row.get("borrowings", 0)
            total_assets = bs_row.get("total_assets", 0)

            # Shares proxy
            shares_outstanding = equity_capital

            # Cash Flow
            cfo = cf_row.get(
                "cash_from_operating_activity", 0
            )

            capex = cf_row.get(
                "capital_expenditure", 0
            )

            dividend_paid = cf_row.get(
                "dividend_paid", 0
            )

            # Core ratios
            npm = validate_ratio(
                net_profit_margin(net_profit, sales),
                "NPM",
                company,
                year
            )

            opm = validate_ratio(
                operating_profit_margin(
                    operating_profit,
                    sales
                ),
                "OPM",
                company,
                year
            )

            roe_value = validate_ratio(
                roe(
                    net_profit,
                    equity_capital,
                    reserves
                ),
                "ROE",
                company,
                year
            )

            de_ratio = validate_ratio(
                debt_to_equity(
                    debt,
                    equity
                ),
                "DE",
                company,
                year
            )

            icr = validate_ratio(
                interest_coverage(
                    operating_profit,
                    interest
                ),
                "ICR",
                company,
                year
            )

            asset_turn = validate_ratio(
                asset_turnover(
                    sales,
                    total_assets
                ),
                "ASSET_TURNOVER",
                company,
                year
            )

            # Cash flow
            fcf = free_cash_flow(cfo, capex)

            # Per-share metrics
            eps = earnings_per_share(
                net_profit,
                shares_outstanding
            )

            bvps = book_value_per_share(
                equity_capital,
                reserves,
                shares_outstanding
            )

            dividend_payout = dividend_payout_ratio(
                dividend_paid,
                net_profit
            )

            total_debt_cr = debt

            # Rolling CAGR
            revenue_cagr = None
            pat_cagr = None
            eps_cagr = None

            if i >= 5:

                start_row = company_pl.iloc[i - 5]
                end_row = company_pl.iloc[i]

                revenue_cagr = calculate_cagr(
                    start_row["sales"],
                    end_row["sales"],
                    5
                )[0]

                pat_cagr = calculate_cagr(
                    start_row["net_profit"],
                    end_row["net_profit"],
                    5
                )[0]

                start_eps = earnings_per_share(
                    start_row["net_profit"],
                    shares_outstanding
                )

                end_eps = earnings_per_share(
                    end_row["net_profit"],
                    shares_outstanding
                )

                eps_cagr = calculate_cagr(
                    start_eps,
                    end_eps,
                    5
                )[0]

            # Composite quality score
            composite_quality_score = round(
                (
                    (roe_value or 0)
                    + (npm or 0)
                    + (opm or 0)
                ) / 3,
                2
            )

            record = {
                "company_id": company,
                "year": year,
                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,
                "return_on_equity_pct": roe_value,
                "debt_to_equity": de_ratio,
                "interest_coverage": icr,
                "asset_turnover": asset_turn,
                "free_cash_flow_cr": fcf,
                "capex_cr": capex,
                "earnings_per_share": eps,
                "book_value_per_share": bvps,
                "dividend_payout_ratio_pct": dividend_payout,
                "total_debt_cr": total_debt_cr,
                "cash_from_operations_cr": cfo,
                "revenue_cagr_5yr": revenue_cagr,
                "pat_cagr_5yr": pat_cagr,
                "eps_cagr_5yr": eps_cagr,
                "composite_quality_score": composite_quality_score
            }

            records.append(record)

    ratios_df = pd.DataFrame(records)

    ratios_df.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print(
        f"Financial ratios table saved successfully. Rows: {len(ratios_df)}"
    )


if __name__ == "__main__":
    generate_financial_ratios()