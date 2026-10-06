# Source data dictionary

The project uses the eight fields in the public UCI Online Retail workbook.

| Field | Meaning | Project use |
| --- | --- | --- |
| `InvoiceNo` | Invoice identifier | Cancellations are invoice numbers beginning with `C`; used for invoice counts. |
| `StockCode` | Product code | Retained for source-row identity. |
| `Description` | Product description | Retained for source-row identity. |
| `Quantity` | Units on the line | Must be greater than zero for an eligible sales line. |
| `InvoiceDate` | Invoice timestamp | Used for monthly aggregation. |
| `UnitPrice` | Unit price in GBP | Must be greater than zero; multiplied by quantity. |
| `CustomerID` | Customer identifier | Not exported or used in the sales dashboard aggregate. |
| `Country` | Customer country | Used for geography summaries. |

`Gross invoiced sales = Quantity × UnitPrice` after the documented exact-duplicate and eligibility rules. It is not net revenue or profit.
