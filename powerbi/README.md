# Power BI build materials

This folder contains the documented build specification and DAX measures for reproducing the report in Power BI Desktop.

## Use the public source

1. Download `Online Retail.xlsx` using [`../data/README.md`](../data/README.md).
2. In Power BI Desktop, choose **Get Data → Excel** and load the workbook.
3. In Power Query, apply the documented cleaning rule before loading the model:
   - remove extra exact duplicate rows, retaining the first occurrence;
   - retain `Quantity > 0` and `UnitPrice > 0`;
   - exclude `InvoiceNo` values beginning with `C`.
4. Name the loaded table `Eligible Sales`.
5. Create the measures in [`measures.dax`](measures.dax), then follow [`dashboard-spec.md`](dashboard-spec.md).

The raw workbook and a `.pbix` file are not committed. The public source file is downloaded separately, and the live HTML dashboard is available through GitHub Pages after deployment.
