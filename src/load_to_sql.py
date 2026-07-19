"""
File: load_to_sql.py
Topic: Load raw CSV data into SQLite database
Author: Noman Rizvi
Project: Sales Data Analysis Pipeline
"""

import os
import sqlite3
import pandas as pd


def load_csv_to_sql(csv_path, db_path, table_name="sales"):
    """
    Read CSV file and load it into a SQLite database.

    Parameters:
        csv_path (str): Path to CSV file
        db_path (str): Path to SQLite database
        table_name (str): SQLite table name
    """

    # Read CSV
    df = pd.read_csv(csv_path)

    # Verify data
    print("\n========== CSV INFORMATION ==========")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    # Create database connection
    conn = sqlite3.connect(db_path)

    # Load DataFrame into SQLite
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("\n========== SUCCESS ==========")
    print(f"{len(df)} rows loaded into '{table_name}' table.")
    print(f"Database saved at: {db_path}")


if __name__ == "__main__":

    # Current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Project root (src -> project folder)
    project_root = os.path.dirname(current_dir)

    # Paths
    csv_path = os.path.join(
        project_root,
        "data",
        "raw",
        "superstore_sales.csv"
    )

    db_path = os.path.join(
        project_root,
        "database",
        "sales.db"
    )

    load_csv_to_sql(csv_path, db_path)