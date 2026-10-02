# Online Retail Sales Analysis

An exploratory analysis of the public **UCI Online Retail** dataset for a UK-based online retailer. The project turns raw transaction lines into a documented sales view, with explicit cleaning rules and reproducible output.

## Business question

What is the scale of eligible invoice activity, and how concentrated is gross invoiced sales by country?

## Dataset

- **Source:** [UCI Machine Learning Repository — Online Retail](https://doi.org/10.24432/C5BW33)
- **Context:** Transactions from a UK-based non-store online retailer, December 2010 to December 2011
- **License:** CC BY 4.0
- **Currency:** GBP (£). The dataset is from a UK retailer, so the project reports monetary values in pounds.

The source workbook is deliberately not committed to this repository. See [data/README.md](data/README.md) for download and placement instructions.

## Approach

1. Loaded and validated the expected eight-column source schema.
2. Removed 5,268 extra exact duplicate rows, retaining the first occurrence.
3. Kept sales lines where `Quantity > 0`, `UnitPrice > 0`, and `InvoiceNo` does not begin with `C` (a cancellation prefix).
4. Calculated **gross invoiced sales** as `Quantity × UnitPrice` and summarized eligible invoice activity by country.
5. Checked the output against the published project benchmarks before writing the JSON summary.

## Key results

| Metric | Result |
| --- | ---: |
| Raw transaction rows | 541,909 |
| Extra exact duplicate rows removed | 5,268 |
| Eligible transaction lines | 524,878 |
| Gross invoiced sales | £10,642,110.80 |
| Distinct eligible invoices | 19,960 |
| Countries represented | 38 |
| United Kingdom share of gross invoiced sales | 84.6% |

The United Kingdom accounts for most gross invoiced sales in this historical dataset, indicating geographic concentration in the observed transaction mix.

## Important interpretation notes

- **£10,642,110.80 is gross invoiced sales, not company revenue or profit.** The measure excludes cancellations and nonpositive quantity or price lines, but it does not include costs, returns reconciliation, taxes, or margin.
- Results describe a public historical dataset from one UK retailer. They are portfolio findings, not results from an employer.
- Exact duplicate removal is a documented analytical rule because the source has no unique transaction-line identifier.

## Repository structure

```text
.
├── data/
│   └── README.md                     # Dataset download and placement instructions
├── outputs/
│   └── summary_metrics.json          # Verified aggregate results; no customer data
├── sql/
│   └── quality_and_sales_summary.sql # SQL equivalent of the key cleaning logic
├── src/
│   └── analyze_retail_sales.py       # Reproducible analysis script
├── .gitignore
├── requirements.txt
└── README.md
```

## Run the analysis

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download the public workbook as data/Online Retail.xlsx first.
python src/analyze_retail_sales.py \
  --input "data/Online Retail.xlsx" \
  --output outputs/summary_metrics.json
```

The script prints the calculated metrics and writes the same aggregate values to `outputs/summary_metrics.json`. It never exports customer-level data.

## Skills demonstrated

Python, pandas, data profiling, duplicate handling, transaction eligibility rules, KPI definition, SQL, and reproducible reporting.
