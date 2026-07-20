"""
File: analyze.py
Topic: Sales Data Analysis
Author: Noman Rizvi
Project: Sales Data Analysis Pipeline
"""

import os
import numpy as np
import pandas as pd


def analyze_sales_data(csv_path):
    """
    Read cleaned sales data and perform analysis.
    """

    # Read cleaned CSV
    df = pd.read_csv(csv_path)

    # Convert Order Date back to datetime
    # CSV stores dates as text, so convert again.
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%Y-%m-%d"
    )

    # ==================================================
    # Monthly Revenue
    # ==================================================

    df["order_month"] = df["Order Date"].dt.to_period("M")

    monthly_revenue = (
        df.groupby("order_month")["Sales"]
        .sum()
    )

    print("\n========== MONTHLY REVENUE ==========")
    print(monthly_revenue)

    # ==================================================
    # Month-over-Month Growth
    # ==================================================

    revenue = monthly_revenue.values

    growth_rate = (
        np.diff(revenue) / revenue[:-1]
    ) * 100

    growth_rate = np.round(growth_rate, 2)

    print("\n========== MONTHLY GROWTH RATE (%) ==========")
    print(growth_rate)

    # ==================================================
    # Top 10 Products
    # ==================================================

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n========== TOP 10 PRODUCTS ==========")
    print(top_products)

    # ==================================================
    # Sales Statistics
    # ==================================================

    sales = df["Sales"].values

    mean_sales = np.mean(sales)
    median_sales = np.median(sales)
    std_sales = np.std(sales)

    print("\n========== SALES STATISTICS ==========")
    print(f"Mean   : {mean_sales:.2f}")
    print(f"Median : {median_sales:.2f}")
    print(f"Std Dev: {std_sales:.2f}")

# ==================================================
# Summary Results
# ==================================================

    total_revenue = df["Sales"].sum()
    average_sale = mean_sales

    # Total rows in the dataset
    total_rows = len(df)

    # Total unique orders
    total_orders = df["Order ID"].nunique()

    top_product = top_products.index[0]
    best_month = monthly_revenue.idxmax()

    print("\n========== ORDER SUMMARY ==========")
    print(f"Total Rows   : {total_rows}")
    print(f"Total Orders : {total_orders}")

    return {
    "total_revenue": total_revenue,
    "average_sale": average_sale,
    "total_rows": total_rows,
    "total_orders": total_orders,
    "top_product": top_product,
    "best_month": str(best_month),
    "monthly_revenue": monthly_revenue,
    "growth_rate": growth_rate,
    "top_products": top_products,
    "mean": mean_sales,
    "median": median_sales,
    "std": std_sales,
    }


if __name__ == "__main__":

    # Current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Project root
    project_root = os.path.dirname(current_dir)

    # Clean CSV path
    csv_path = os.path.join(
        project_root,
        "data",
        "processed",
        "clean_sales.csv"
    )

    results = analyze_sales_data(csv_path)