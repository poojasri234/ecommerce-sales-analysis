# Dashboard data

`data.json` contains aggregate monthly-country metrics used by the live dashboard. It includes no transaction-line or customer-level records.

Fields:

- `month`: calendar month in `YYYY-MM` format
- `country`: country reported in the public source workbook
- `gross_invoiced_sales_gbp`: `Quantity × UnitPrice` after the documented cleaning rule
- `eligible_transaction_lines`: positive, non-cancelled, deduplicated lines
- `distinct_eligible_invoices`: distinct retained invoice numbers

The raw source workbook is intentionally not included. Download instructions are in [`../data/README.md`](../data/README.md).
