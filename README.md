# E-commerce Sales Analysis

[Open the live dashboard](https://poojasri234.github.io/ecommerce-sales-analysis/)

**Tools:** Python/pandas · SQL/SQLite · Excel source-data handling · interactive HTML dashboard · Power BI report specification and DAX measures

A reproducible case study using the public [UCI Online Retail dataset](https://doi.org/10.24432/C5BW33): a UK-based non-store retailer's transactions from December 2010 to December 2011. Values are reported in GBP (£).

## Business question

After applying transparent transaction-quality rules, what is the scale of eligible invoice activity and where is gross invoiced sales concentrated?

## Approach

1. Validated the source workbook's eight expected fields.
2. Removed **5,268** extra exact full-row copies, retaining the first occurrence.
3. Defined an eligible sales line as `Quantity > 0`, `UnitPrice > 0`, and an `InvoiceNo` that does not begin with `C`.
4. Defined **gross invoiced sales** as `Quantity × UnitPrice` for eligible lines.
5. Reproduced the cleaning logic and KPI aggregation in [SQL](sql/quality_and_sales_summary.sql), then documented matching [Power BI measures](powerbi/measures.dax) and validation checks.

## Findings

| Metric | Result |
| --- | ---: |
| Raw transaction rows | 541,909 |
| Extra exact duplicate rows removed | 5,268 |
| Eligible transaction lines | 524,878 |
| Gross invoiced sales | £10,642,110.80 |
| Distinct eligible invoices | 19,960 |
| Countries represented | 38 |
| UK share of gross invoiced sales | 84.6% |

The historical sales mix is highly concentrated in the United Kingdom: about **£9.0M** of the observed gross-invoice base came from the UK.

## Recommendation

Use a monthly country-level monitoring view that separates UK and international sales. Because the UK drives most of the historical baseline, investigate UK mix changes first before acting on aggregate sales movement.

Before making an expansion or marketing decision, add returns reconciliation, product margin, delivery cost, and repeat-purchase measures. Country-level gross invoiced sales alone cannot identify the most profitable or highest-growth opportunity.

## Potential business value — illustrative only

A **1% relative movement in the historical UK gross-invoice base** is roughly **£90K** of invoice volume. This is arithmetic sizing for prioritisation only; it is not a forecast, net revenue, profit, or expected campaign return.

## Limitations

- Gross invoiced sales is not net revenue or profit; the source does not include cost, tax, margin, or a full returns reconciliation.
- This is one historical public dataset from a UK-based retailer, not employer data.
- The source has no transaction-line identifier. Exact-duplicate removal is a documented analytical assumption and could remove a genuinely repeated identical line.
- Do not compare partial periods with full months without checking source-date coverage.

## SQL and dashboard evidence

- [`sql/quality_and_sales_summary.sql`](sql/quality_and_sales_summary.sql) — deduplication, eligibility CTE, KPI and country-mix queries.
- [`src/analyze_retail_sales.py`](src/analyze_retail_sales.py) — reproducible analysis and validation.
- [`powerbi/`](powerbi/) — DAX measures, visual specification, and import guide. A completed `.pbix` file is not included.
- [`outputs/summary_metrics.json`](outputs/summary_metrics.json) — aggregate-only verified output.

## 3-minute interview walkthrough

- **0:00–0:25:** Frame the decision: establish a trustworthy gross-sales baseline and identify country concentration.
- **0:25–0:55:** Explain the eight-field schema check, the 5,268 exact duplicates, and the cancellation/positive-value eligibility rules.
- **0:55–1:25:** Define gross invoiced sales clearly and distinguish it from revenue and profit.
- **1:25–1:55:** State the result: £10.64M across 19,960 eligible invoices; 84.6% of the observed gross-invoice base is UK.
- **1:55–2:30:** Recommend country-mix monitoring and explain why returns, margin, and delivery cost are required before a commercial decision.
- **2:30–3:00:** Show the SQL CTE and Power BI specification. With production data, add a transaction-line key, return reconciliation, margins, product mix, and repeat-purchase analysis.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download the public UCI workbook as data/Online Retail.xlsx first.
python src/analyze_retail_sales.py \
  --input "data/Online Retail.xlsx" \
  --output outputs/summary_metrics.json
```

The raw workbook is not committed. See [data/README.md](data/README.md) for source and placement instructions.
