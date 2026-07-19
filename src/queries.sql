/*
File: queries.sql
Topic: SQL Analysis Queries
Author: Noman Rizvi
Project: Sales Data Analysis Pipeline
*/

-- ==========================================================
-- 1. Business Question:
-- What is the total sales revenue?
-- ==========================================================
SELECT SUM(Sales) AS total_sales
FROM sales;


-- ==========================================================
-- 2. Business Question:
-- What is the total sales for each category?
-- (Highest to Lowest)
-- ==========================================================
SELECT
    Category,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;


-- ==========================================================
-- 3. Business Question:
-- Which are the Top 5 Sub-Categories by sales?
-- ==========================================================
SELECT
    "Sub-Category",
    SUM(Sales) AS total_sales
FROM sales
GROUP BY "Sub-Category"
ORDER BY total_sales DESC
LIMIT 5;


-- ==========================================================
-- 4. Business Question:
-- What are the total and average sales in each region?
-- ==========================================================
SELECT
    Region,
    SUM(Sales) AS total_sales,
    AVG(Sales) AS average_sales
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;


-- ==========================================================
-- 5. Business Question:
-- Who are the Top 10 customers by total spending?
-- ==========================================================
SELECT
    "Customer Name",
    SUM(Sales) AS total_spending
FROM sales
GROUP BY "Customer Name"
ORDER BY total_spending DESC
LIMIT 10;


-- ==========================================================
-- 6. Business Question:
-- Which customer segment generates the most revenue?
-- ==========================================================
SELECT
    Segment,
    SUM(Sales) AS total_sales
FROM sales
GROUP BY Segment
ORDER BY total_sales DESC;


-- ==========================================================
-- 7. Business Question:
-- How many unique orders are there in each state?
-- ==========================================================
SELECT
    State,
    COUNT(DISTINCT "Order ID") AS unique_orders
FROM sales
GROUP BY State
ORDER BY unique_orders DESC;


-- ==========================================================
-- 8. Business Question:
-- Which single order has the highest sales?
-- ==========================================================
SELECT *
FROM sales
WHERE Sales = (
    SELECT MAX(Sales)
    FROM sales
);


-- ==========================================================
-- 9. Business Question:
-- What is the average sales for each shipping mode?
-- ==========================================================
SELECT
    "Ship Mode",
    AVG(Sales) AS average_sales
FROM sales
GROUP BY "Ship Mode"
ORDER BY average_sales DESC;


-- ==========================================================
-- 10. Business Question:
-- Which Top 5 products were ordered the most?
-- ==========================================================
SELECT
    "Product Name",
    COUNT(*) AS total_orders
FROM sales
GROUP BY "Product Name"
ORDER BY total_orders DESC
LIMIT 5;