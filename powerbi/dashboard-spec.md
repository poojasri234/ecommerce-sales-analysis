# Power BI dashboard specification

## Model

Use one cleaned fact table named `Eligible Sales`. Create an optional calendar table related to `Eligible Sales[InvoiceDate]` for month filtering.

## Report page: Sales overview

1. Add cards for `Gross Invoiced Sales`, `Eligible Transaction Lines`, `Distinct Eligible Invoices`, and `Countries Represented`.
2. Add a line chart with calendar month on the x-axis and `Gross Invoiced Sales` on the y-axis.
3. Add a horizontal bar chart with `Country` and `Gross Invoiced Sales`, sorted descending.
4. Add a country slicer and a month range slicer.
5. Add a text note: **Gross invoiced sales is not net revenue or profit.**

## Validation checks

The cleaned model should reconcile to these published aggregate results:

- 524,878 eligible transaction lines
- £10,642,110.80 gross invoiced sales
- 19,960 distinct eligible invoices
- 38 countries
- 84.6% United Kingdom share of gross invoiced sales
