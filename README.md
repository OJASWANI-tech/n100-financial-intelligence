# 📊 N100 Financial Intelligence Platform

A production-grade financial analytics platform built to analyze **92 Nifty 100 companies** using structured financial datasets, automated KPI engines, screening models, and interactive dashboards.

This project transforms raw company financial data into a complete intelligence system for evaluating profitability, financial health, valuation, sector performance, and peer benchmarking.

---

## 🚀 Overview

The **N100 Financial Intelligence Platform** is designed as a complete financial analytics ecosystem that processes multi-year company financial statements and generates actionable investment insights.

The system ingests raw financial datasets including:

* Profit & Loss Statements
* Balance Sheets
* Cash Flow Statements
* Sector Classifications
* Market Capitalization Data
* Stock Price History
* Peer Groups
* Financial Ratios
* Company Reports

The platform enables analysts to perform structured company analysis without relying on third-party paid tools.

---

## ✨ Key Features

### ⚙️ Data Engineering & ETL

* Automated ingestion of **12 structured datasets**
* Data normalization and cleaning pipeline
* SQLite data warehouse integration
* Schema validation and audit logging

---

### 📈 Financial KPI Engine

Compute **30+ key financial metrics**, including:

* Return on Equity (ROE)
* Return on Capital Employed (ROCE)
* Net Profit Margin (NPM)
* Operating Profit Margin (OPM)
* Debt-to-Equity Ratio
* Interest Coverage Ratio
* Asset Turnover Ratio
* Free Cash Flow (FCF)
* Earnings Per Share (EPS)
* Book Value Per Share
* CAGR (1Y / 3Y / 5Y / 10Y)

---

### 🔍 Investment Screener

Advanced stock screening system with:

* **18 configurable filters**
* Quality growth filters
* Debt-free filters
* Turnaround stock detection
* High ROE / ROCE filters
* Cash flow strength filters

---

### 💡 Financial Health Score (0–100)

A custom composite scoring engine to evaluate company strength:

| Score Range | Status    |
| ----------- | --------- |
| 80–100      | Excellent |
| 65–79       | Good      |
| 50–64       | Average   |
| 35–49       | Weak      |
| 0–34        | Poor      |

---

### 🏢 Sector Analytics

Sector-wise benchmarking across **11 broad sectors**:

* Financials
* Information Technology
* Energy
* Consumer Staples
* Consumer Discretionary
* Healthcare
* Materials
* Industrials
* Communication Services
* Real Estate
* Conglomerates

---

### 📊 Peer Comparison Engine

Compare companies against peer groups using:

* Percentile rankings
* KPI benchmarking
* Best-in-class analysis
* Radar chart visualization

---

### 📄 Automated Reporting

Generate:

* Individual company reports (PDF)
* Sector reports (PDF)
* Full universe Excel reports
* Screener exports

---

### 🌐 Interactive Dashboard

Built with **Streamlit** for:

* Company profile view
* KPI visualization
* Screener execution
* Sector comparisons
* Health score analysis
* Peer intelligence

---

## 🛠 Tech Stack

### Programming & Data Processing

* Python
* Pandas
* NumPy

### Database

* SQLite
* SQLAlchemy

### Visualization

* Plotly
* Matplotlib
* Streamlit

### Reporting

* ReportLab
* OpenPyXL

### Testing

* Pytest
* Pytest-Cov

---

## 📂 Project Structure

```text
n100-financial-intelligence/
│── data/
│   ├── raw/
│   ├── processed/
│
│── db/
│   ├── schema.sql
│
│── src/
│   ├── etl/
│   ├── ratios/
│   ├── screener/
│   ├── scoring/
│   ├── sector/
│   ├── peers/
│   ├── reports/
│   ├── dashboard/
│
│── tests/
│
│── output/
│
│── notebooks/
│
│── README.md
│── requirements.txt
│── Makefile
```

---

## 📊 Dataset Coverage

| Dataset          | Records |
| ---------------- | ------- |
| Companies        | 92      |
| Profit & Loss    | 1,276   |
| Balance Sheet    | 1,312   |
| Cash Flow        | 1,187   |
| Documents        | 1,585   |
| Stock Prices     | 5,520   |
| Financial Ratios | 1,184   |
| Market Cap       | 552     |

Total Data Points: **11,000+**

---

## 🔬 Testing & Quality Assurance

The platform follows production-grade quality standards:

* 35+ Unit Tests
* Data Quality Validation Rules
* Foreign Key Integrity Checks
* Schema Validation
* Audit Logs

Target Coverage: **80%+**

---

## 📌 Project Goals

* Build a unified financial intelligence system for Nifty 100 companies
* Automate fundamental analysis workflows
* Reduce manual analysis effort
* Create reproducible financial reports
* Enable faster investment decision-making

---

## 📈 Future Enhancements

* Real-time stock price APIs
* Portfolio tracking module
* Watchlist & alerts
* Financial news integration
* AI-based insights engine
* Stock recommendation system

---

## 👩‍💻 Author

**Ojaswani**
Data Analyst | Python | SQL | Power BI | Financial Analytics

GitHub: https://github.com/OJASWANI-tech
