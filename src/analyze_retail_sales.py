#!/usr/bin/env python3
"""Create an aggregate sales summary from UCI's Online Retail workbook.

Usage:
    python src/analyze_retail_sales.py \
        --input "data/Online Retail.xlsx" \
        --output outputs/summary_metrics.json

The script reads a local copy of the public workbook, applies the documented
cleaning rules, writes aggregate metrics only, and checks that the official
source workbook reproduces the portfolio benchmarks.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

import pandas as pd


EXPECTED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]

# These checks protect the public portfolio claims for the official UCI workbook.
EXPECTED_BENCHMARKS = {
    "raw_transaction_rows": 541_909,
    "exact_duplicate_rows_removed": 5_268,
    "eligible_transaction_lines": 524_878,
    "gross_invoiced_sales_gbp": Decimal("10642110.80"),
    "distinct_eligible_invoices": 19_960,
    "countries_represented": 38,
    "united_kingdom_gross_invoiced_sales_share_percent": Decimal("84.6"),
}


def money(value: object) -> Decimal:
    """Convert a numeric value through its string representation for safe rounding."""
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def percentage(numerator: Decimal, denominator: Decimal) -> Decimal:
    """Return a one-decimal percentage; denominator must be positive."""
    if denominator <= 0:
        raise ValueError("Cannot calculate a percentage with a non-positive denominator.")
    return (numerator * Decimal("100") / denominator).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )


def validate_schema(frame: pd.DataFrame) -> None:
    """Fail early if the workbook is not the expected UCI Online Retail schema."""
    if frame.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(
            "Unexpected workbook schema. Expected columns in this order: "
            + ", ".join(EXPECTED_COLUMNS)
        )
    required = ["InvoiceNo", "Quantity", "InvoiceDate", "UnitPrice", "Country"]
    if frame[required].isna().any().any():
        raise ValueError("Required transaction fields contain missing values.")


def calculate_metrics(input_path: Path) -> dict[str, Any]:
    """Read, clean and summarize the source workbook without exporting raw data."""
    if not input_path.is_file():
        raise FileNotFoundError(
            f"Workbook not found: {input_path}. See data/README.md for download instructions."
        )

    raw = pd.read_excel(
        input_path,
        engine="openpyxl",
        dtype={"InvoiceNo": str, "StockCode": str},
    )
    validate_schema(raw)
    raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"], errors="raise")

    # Remove extra full-row copies. The original source row is retained.
    duplicate_rows = raw.duplicated(keep="first")
    deduplicated = raw.loc[~duplicate_rows].copy()

    # Define an eligible sales line. Anonymous customer lines remain in sales totals.
    cancelled = deduplicated["InvoiceNo"].str.upper().str.startswith("C")
    eligible = (
        (deduplicated["Quantity"] > 0)
        & (deduplicated["UnitPrice"] > 0)
        & ~cancelled
    )
    sales = deduplicated.loc[eligible].copy()
    sales["gross_invoiced_sales_gbp"] = sales["Quantity"] * sales["UnitPrice"]

    gross_sales = money(sales["gross_invoiced_sales_gbp"].sum())
    uk_sales = money(
        sales.loc[sales["Country"] == "United Kingdom", "gross_invoiced_sales_gbp"].sum()
    )

    return {
        "project": "Online Retail Sales Analysis",
        "source": {
            "name": "UCI Online Retail",
            "url": "https://doi.org/10.24432/C5BW33",
            "license": "CC BY 4.0",
            "retailer_context": "UK-based non-store online retailer",
        },
        "currency": "GBP",
        "metric_definition": (
            "Gross invoiced sales = Quantity × UnitPrice for deduplicated, "
            "positive-quantity, positive-unit-price, non-cancellation invoice lines."
        ),
        "metrics": {
            "raw_transaction_rows": int(len(raw)),
            "exact_duplicate_rows_removed": int(duplicate_rows.sum()),
            "eligible_transaction_lines": int(len(sales)),
            "gross_invoiced_sales_gbp": float(gross_sales),
            "distinct_eligible_invoices": int(sales["InvoiceNo"].nunique()),
            "countries_represented": int(sales["Country"].nunique()),
            "united_kingdom_gross_invoiced_sales_share_percent": float(
                percentage(uk_sales, gross_sales)
            ),
        },
        "interpretation_notes": [
            "Gross invoiced sales is not net revenue or profit.",
            "Results describe a public historical dataset and are not employer results.",
        ],
    }


def verify_benchmarks(result: dict[str, Any]) -> None:
    """Raise a clear error if the selected workbook does not match the official source."""
    metrics = result["metrics"]
    actual = {
        "raw_transaction_rows": metrics["raw_transaction_rows"],
        "exact_duplicate_rows_removed": metrics["exact_duplicate_rows_removed"],
        "eligible_transaction_lines": metrics["eligible_transaction_lines"],
        "gross_invoiced_sales_gbp": money(metrics["gross_invoiced_sales_gbp"]),
        "distinct_eligible_invoices": metrics["distinct_eligible_invoices"],
        "countries_represented": metrics["countries_represented"],
        "united_kingdom_gross_invoiced_sales_share_percent": Decimal(
            str(metrics["united_kingdom_gross_invoiced_sales_share_percent"])
        ),
    }
    mismatches = {
        key: {"expected": str(expected), "actual": str(actual[key])}
        for key, expected in EXPECTED_BENCHMARKS.items()
        if actual[key] != expected
    }
    if mismatches:
        raise ValueError(
            "The selected workbook did not reproduce the expected UCI project benchmarks: "
            + json.dumps(mismatches, indent=2)
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to Online Retail.xlsx")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/summary_metrics.json"),
        help="Path for aggregate JSON output (default: outputs/summary_metrics.json)",
    )
    parser.add_argument(
        "--skip-verification",
        action="store_true",
        help="Write calculated metrics without checking official UCI benchmarks.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = calculate_metrics(args.input)
    if not args.skip_verification:
        verify_benchmarks(result)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    metrics = result["metrics"]
    print("Analysis complete")
    print(f"Raw transaction rows: {metrics['raw_transaction_rows']:,}")
    print(f"Exact duplicate rows removed: {metrics['exact_duplicate_rows_removed']:,}")
    print(f"Eligible transaction lines: {metrics['eligible_transaction_lines']:,}")
    print(f"Gross invoiced sales: £{metrics['gross_invoiced_sales_gbp']:,.2f}")
    print(f"Distinct eligible invoices: {metrics['distinct_eligible_invoices']:,}")
    print(f"Countries represented: {metrics['countries_represented']}")
    print(
        "United Kingdom share of gross invoiced sales: "
        f"{metrics['united_kingdom_gross_invoiced_sales_share_percent']:.1f}%"
    )
    print(f"Wrote aggregate results to: {args.output}")


if __name__ == "__main__":
    main()
