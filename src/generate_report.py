"""
File: generate_report.py
Topic: Generate Sales Report
Author: Noman Rizvi
Project: Sales Data Analysis Pipeline
"""

import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from analyze import analyze_sales_data


def generate_report(csv_path, summary_csv, report_txt, report_pdf):

    # Get analysis results
    results = analyze_sales_data(csv_path)

    # ==========================================
    # Summary CSV
    # ==========================================

    summary = pd.DataFrame({
        "metric_name": [
            "Total Revenue",
            "Average Sale",
            "Total Orders",
            "Top Product",
            "Best Month"
        ],
        "value": [
            results["total_revenue"],
            results["average_sale"],
            results["total_orders"],
            results["top_product"],
            results["best_month"]
        ]
    })

    summary.to_csv(summary_csv, index=False)

    # ==========================================
    # Text Report
    # ==========================================

    report = f"""SALES ANALYSIS REPORT
==============================

Total Revenue : {results['total_revenue']:.2f}
Average Sale  : {results['average_sale']:.2f}
Total Orders  : {results['total_orders']}
Top Product   : {results['top_product']}
Best Month    : {results['best_month']}

Sales Statistics
----------------
Mean   : {results['mean']:.2f}
Median : {results['median']:.2f}
Std Dev: {results['std']:.2f}

Top 10 Products
---------------
"""

    for product, value in results["top_products"].items():
        report += f"{product} : {value:.2f}\n"

    report += "\nMonthly Revenue\n---------------\n"

    for month, revenue in results["monthly_revenue"].items():
        report += f"{month} : {revenue:.2f}\n"

    with open(report_txt, "w") as file:
        file.write(report)

    # ==========================================
    # PDF Report (ReportLab)
    # ==========================================

    doc = SimpleDocTemplate(report_pdf)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "Sales Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Summary
    story.append(
        Paragraph("<b>Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Total Revenue: {results['total_revenue']:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Average Sale: {results['average_sale']:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Total Orders: {results['total_orders']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Top Product: {results['top_product']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Best Month: {results['best_month']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # Sales Statistics
    story.append(
        Paragraph(
            "<b>Sales Statistics</b>",
            styles["Heading2"]
        )
    )

    stats = [
        ["Metric", "Value"],
        ["Mean", f"{results['mean']:.2f}"],
        ["Median", f"{results['median']:.2f}"],
        ["Standard Deviation", f"{results['std']:.2f}"],
    ]

    stats_table = Table(stats)

    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(stats_table)

    story.append(Spacer(1, 20))

    # Top Products
    story.append(
        Paragraph(
            "<b>Top 10 Products</b>",
            styles["Heading2"]
        )
    )

    product_data = [["Product", "Sales"]]

    for product, value in results["top_products"].items():
        product_data.append([
            product,
            f"{value:.2f}"
        ])

    product_table = Table(product_data)

    product_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(product_table)

    story.append(Spacer(1, 20))

    # Monthly Revenue
    story.append(
        Paragraph(
            "<b>Monthly Revenue</b>",
            styles["Heading2"]
        )
    )

    revenue_data = [["Month", "Revenue"]]

    for month, revenue in results["monthly_revenue"].items():
        revenue_data.append([
            str(month),
            f"{revenue:.2f}"
        ])

    revenue_table = Table(revenue_data)

    revenue_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(revenue_table)

    # Build PDF
    doc.build(story)

    print("\n========== REPORT GENERATED ==========")
    print(f"Summary CSV : {summary_csv}")
    print(f"Text Report : {report_txt}")
    print(f"PDF Report  : {report_pdf}")


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    csv_path = os.path.join(
        project_root,
        "data",
        "processed",
        "clean_sales.csv"
    )

    summary_csv = os.path.join(
        project_root,
        "data",
        "processed",
        "summary_report.csv"
    )

    report_txt = os.path.join(
        project_root,
        "reports",
        "sales_report.txt"
    )

    report_pdf = os.path.join(
        project_root,
        "reports",
        "sales_report.pdf"
    )

    generate_report(
        csv_path,
        summary_csv,
        report_txt,
        report_pdf
    )