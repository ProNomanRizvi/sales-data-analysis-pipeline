"""
File: clean_data.py
Topic: Clean sales data
Author: Noman Rizvi
Project: Sales Data Analysis Pipeline
"""

import os
import sqlite3
import pandas as pd


def clean_sales_data(db_path, output_path):
    """
    Load sales data from SQLite, clean it,
    and save the cleaned data as a CSV file.
    """

    # Connect to SQLite
    conn = sqlite3.connect(db_path)

    # Read data from database
    df = pd.read_sql_query("SELECT * FROM sales", conn)

    conn.close()

    # Check dataset size
    print("\n========== DATA SHAPE ==========")
    print(df.shape)

    # Check missing values
    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    # Fill missing Postal Code values
    # Reason:
    # Postal Code is a numeric identifier.
    # Filling missing values with 0 clearly marks them as missing.
    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].fillna(0)

    # after fillna
    print("\n========== POSTAL CODE AFTER FILL ==========")
    print(df["Postal Code"].isnull().sum())

    # Convert date columns to datetime
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d/%m/%Y"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d/%m/%Y"
    )

    # after date conversion
    print("\n========== DTYPES AFTER DATE CONVERSION ==========")
    print(df[["Order Date", "Ship Date"]].dtypes)

    # Check duplicate rows
    duplicate_rows = df.duplicated().sum()

    print("\n========== DUPLICATE ROWS ==========")
    print(duplicate_rows)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save cleaned data
    df.to_csv(output_path, index=False)

    print("\n========== SUCCESS ==========")
    print(f"Cleaned data saved to:\n{output_path}")
    print(f"Final Shape: {df.shape}")


if __name__ == "__main__":

    # Current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Project root
    project_root = os.path.dirname(current_dir)

    # Database path
    db_path = os.path.join(
        project_root,
        "database",
        "sales.db"
    )

    # Output CSV path
    output_path = os.path.join(
        project_root,
        "data",
        "processed",
        "clean_sales.csv"
    )

    clean_sales_data(db_path, output_path)