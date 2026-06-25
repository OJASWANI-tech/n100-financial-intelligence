-- 1. Total companies
SELECT COUNT(*) FROM companies;

-- 2. Top 10 companies by latest sales
SELECT company_id, sales
FROM profit_loss
WHERE year = 'TTM'
ORDER BY sales DESC
LIMIT 10;

-- 3. Top 10 by net profit
SELECT company_id, net_profit
FROM profit_loss
WHERE year = 'TTM'
ORDER BY net_profit DESC
LIMIT 10;

-- 4. Companies with highest borrowings
SELECT company_id, borrowings
FROM balance_sheet
ORDER BY borrowings DESC
LIMIT 10;

-- 5. Companies with negative operating cash flow
SELECT company_id, operating_activity
FROM cash_flow
WHERE operating_activity < 0;

-- 6. Top dividend payout companies
SELECT company_id, dividend_payout
FROM profit_loss
ORDER BY dividend_payout DESC
LIMIT 10;

-- 7. Highest EPS companies
SELECT company_id, eps
FROM profit_loss
ORDER BY eps DESC
LIMIT 10;

-- 8. Companies with lowest tax %
SELECT company_id, tax_percentage
FROM profit_loss
ORDER BY tax_percentage ASC
LIMIT 10;

-- 9. Sector-wise company count
SELECT sector_name, COUNT(*)
FROM sectors
GROUP BY sector_name;

-- 10. Top asset-heavy companies
SELECT company_id, total_assets
FROM balance_sheet
ORDER BY total_assets DESC
LIMIT 10;
