"""Regression tests for the sales questions, using representative order lines."""

import sqlite3
import unittest
from pathlib import Path


QUERIES = Path(__file__).resolve().parents[1] / "src" / "queries.sql"


class SalesQueryTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.execute(
            """CREATE TABLE sales (
                "Order ID" TEXT,
                "Product Name" TEXT,
                Sales REAL,
                Category TEXT,
                "Sub-Category" TEXT,
                Region TEXT,
                "Customer Name" TEXT,
                Segment TEXT,
                State TEXT,
                "Ship Mode" TEXT
            )"""
        )
        self.connection.executemany(
            """INSERT INTO sales (
                "Order ID", "Product Name", Sales, Category,
                "Sub-Category", Region, "Customer Name", Segment,
                State, "Ship Mode"
            ) VALUES (?, ?, ?, 'Office Supplies', 'Paper', 'West',
                      'Alex', 'Consumer', 'CA', 'Standard Class')""",
            [
                ("O-1", "Alpha", 60),
                ("O-1", "Alpha", 60),
                ("O-2", "Beta", 100),
                ("O-3", "Beta", 10),
            ],
        )
        self.statements = [
            statement.strip()
            for statement in QUERIES.read_text(encoding="utf-8").split(";")
            if statement.strip()
        ]

    def test_all_business_queries_execute(self):
        self.assertEqual(len(self.statements), 10)
        for index, statement in enumerate(self.statements, start=1):
            with self.subTest(question=index):
                self.connection.execute(statement).fetchall()

    def test_highest_sales_order_sums_its_line_items(self):
        # O-2 has the largest line item; O-1 has the largest order total.
        self.assertEqual(
            self.connection.execute(self.statements[7]).fetchall(),
            [("O-1", 120.0)],
        )

    def test_most_ordered_product_counts_distinct_orders(self):
        # Alpha appears twice in one order; Beta appears in two orders.
        self.assertEqual(
            self.connection.execute(self.statements[9]).fetchall(),
            [("Beta", 2), ("Alpha", 1)],
        )


if __name__ == "__main__":
    unittest.main()
