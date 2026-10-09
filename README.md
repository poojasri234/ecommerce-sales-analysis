# E-commerce Sales Analysis

[View the live dashboard](https://poojasri234.github.io/ecommerce-sales-analysis/)

I used the public [UCI Online Retail dataset](https://doi.org/10.24432/C5BW33) to build a clean sales baseline for a UK-based online retailer (December 2010–December 2011). All values are in GBP (£).

## Question

What does eligible invoice activity look like after clear cleaning rules, and where is gross invoiced sales concentrated?

## Method

- Checked the workbook against its eight expected fields.
- Removed **5,268** exact duplicate rows, keeping the first copy.
- Counted a line as eligible when `Quantity > 0`, `UnitPrice > 0`, and the invoice number did not start with `C`.
- Calculated gross invoiced sales as `Quantity × UnitPrice`.
- Recreated the cleaning and aggregation steps in [SQL](sql/quality_and_sales_summary.sql) and checked the results against the Python output.

## Results

| Metric | Result |
| --- | ---: |
| Raw transaction rows | 541,909 |
| Eligible transaction lines | 524,878 |
| Gross invoiced sales | £10,642,110.80 |
| Eligible invoices | 19,960 |
| Countries | 38 |
| UK share of gross invoiced sales | 84.6% |

About **£9.0M** of the historical gross-invoice base came from the UK, so a broad sales movement would be worth checking there first.

## Recommended next step

Use a monthly UK-versus-international view to spot mix changes, then investigate the UK category, product, or customer segments behind a movement. Before using this for an expansion or campaign decision, add returns, margin, delivery cost, and repeat-purchase data.

For scale only, a 1% change in the historical UK gross-invoice base is about **£90K** of invoice volume. That is not a forecast, profit estimate, or expected campaign return.

## Notes on the data

- Gross invoiced sales is not net revenue or profit.
- The dataset is a historical public sample, not company data.
- There is no line-item key, so removing exact duplicates is a documented analytical assumption.
- Check date coverage before comparing a partial period with a full month.

## Project files

- [SQL analysis](sql/quality_and_sales_summary.sql)
- [Python analysis](src/analyze_retail_sales.py)
- [Power BI measures and report plan](powerbi/)
- [Aggregate output](outputs/summary_metrics.json)

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download the public UCI workbook as data/Online Retail.xlsx first.
python src/analyze_retail_sales.py \
  --input "data/Online Retail.xlsx" \
  --output outputs/summary_metrics.json
```

The raw workbook is not committed. [Data instructions](data/README.md) explain where to place it.
