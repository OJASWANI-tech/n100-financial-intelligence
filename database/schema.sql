PRAGMA foreign_keys = ON;

-- Drop child tables first
DROP TABLE IF EXISTS pros_cons;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS peer_groups;
DROP TABLE IF EXISTS market_cap;
DROP TABLE IF EXISTS cash_flow;
DROP TABLE IF EXISTS profit_loss;
DROP TABLE IF EXISTS balance_sheet;
DROP TABLE IF EXISTS financial_ratios;
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS sectors;
DROP TABLE IF EXISTS companies;

---------------------------------------------------
-- 1. Companies (Parent Table)
---------------------------------------------------
CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_logo TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

---------------------------------------------------
-- 2. Sectors
---------------------------------------------------
CREATE TABLE sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 3. Stock Prices
---------------------------------------------------
CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    date TEXT NOT NULL,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 4. Financial Ratios
---------------------------------------------------
CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,
    free_cash_flow_cr REAL,
    capex_cr REAL,
    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,
    total_debt_cr REAL,
    cash_from_operations_cr REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 5. Balance Sheet
---------------------------------------------------
CREATE TABLE balance_sheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_assets REAL,
    total_assets REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 6. Profit and Loss
---------------------------------------------------
CREATE TABLE profit_loss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 7. Cash Flow
---------------------------------------------------
CREATE TABLE cash_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 8. Market Cap
---------------------------------------------------
CREATE TABLE market_cap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    market_cap_crore REAL,
    enterprise_value_crore REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 9. Peer Groups
---------------------------------------------------
CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    peer_group_name TEXT,
    company_id TEXT NOT NULL,
    is_benchmark BOOLEAN,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 10. Documents
---------------------------------------------------
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    year TEXT,
    annual_report TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 11. Analysis
---------------------------------------------------
CREATE TABLE analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

---------------------------------------------------
-- 12. Pros and Cons
---------------------------------------------------
CREATE TABLE pros_cons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT NOT NULL,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);