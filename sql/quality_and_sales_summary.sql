-- Run after importing the public UCI workbook into a table named raw_retail.
-- The query mirrors the Python project rules:
--   1. Keep the first exact copy of each source row.
--   2. Retain positive quantity and UnitPrice values.
--   3. Exclude invoice numbers beginning with C (cancellations).
-- Monetary results are GBP gross invoiced sales, not net revenue or profit.

WITH deduplicated AS (
    SELECT DISTINCT
        InvoiceNo,
        StockCode,
        Description,
        Quantity,
        InvoiceDate,
        UnitPrice,
        CustomerID,
        Country
    FROM raw_retail
),
eligible_sales AS (
    SELECT *
    FROM deduplicated
    WHERE Quantity > 0
      AND UnitPrice > 0
      AND UPPER(InvoiceNo) NOT LIKE 'C%'
)
SELECT
    COUNT(*) AS eligible_transaction_lines,
    COUNT(DISTINCT InvoiceNo) AS distinct_eligible_invoices,
    COUNT(DISTINCT Country) AS countries_represented,
    ROUND(SUM(Quantity * UnitPrice), 2) AS gross_invoiced_sales_gbp,
    ROUND(
        100.0 * SUM(CASE WHEN Country = 'United Kingdom' THEN Quantity * UnitPrice ELSE 0 END)
        / SUM(Quantity * UnitPrice),
        1
    ) AS united_kingdom_gross_invoiced_sales_share_percent
FROM eligible_sales;
