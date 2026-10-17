-- build_etl_demo.sql
-- Builds the whole example ETL in one go: source data, lake, warehouse and report.
-- Safe to run again. It replaces the tables each time.
--
-- Run it in the DuckDB UI: paste it into a cell and run it.
-- Or from the terminal:
--   duckdb etl_demo.duckdb -c ".read tests/etl/build_etl_demo.sql"


-- 1. Source data: the raw customers and transactions, as they arrive
CREATE OR REPLACE TABLE src_customers AS
SELECT * FROM (VALUES
  (1, 'Priya Nair', 'NSW'),
  (2, 'Tom Baker', 'VIC'),
  (3, 'Ana Costa', 'nsw'),
  (4, 'Li Wei', 'QLD'),
  (5, 'Sam Ortiz', 'VIC')
) AS t(customer_id, name, state);

CREATE OR REPLACE TABLE src_transactions AS
SELECT * FROM (VALUES
  (101, 1, '2026-09-03', '120.50', 'completed'),
  (102, 2, '2026-09-05', '$75.00', 'completed'),
  (103, 3, '2026-09-12', '300.00', 'COMPLETED'),
  (104, 1, '2026-09-20', '45.25', 'pending'),
  (105, 4, '2026-10-02', '210.00', 'completed'),
  (106, 5, '2026-10-04', '$89.90', 'completed'),
  (107, 2, '2026-10-09', '150.00', 'refunded'),
  (108, 3, '2026-10-15', '60.00', 'completed')
) AS t(txn_id, customer_id, txn_date, amount, status);


-- 2. Extract: copy the source into the lake, exactly as it is
CREATE OR REPLACE TABLE lake_customers AS SELECT * FROM src_customers;
CREATE OR REPLACE TABLE lake_transactions AS SELECT * FROM src_transactions;


-- 3. Transform and load: clean it, join it, keep completed ones, load the warehouse
CREATE OR REPLACE TABLE wh_transactions AS
SELECT t.txn_id,
       t.customer_id,
       c.name AS customer_name,
       upper(c.state) AS state,
       CAST(t.txn_date AS DATE) AS txn_date,
       CAST(replace(t.amount, '$', '') AS DECIMAL(10, 2)) AS amount
FROM lake_transactions t
JOIN lake_customers c ON c.customer_id = t.customer_id
WHERE lower(t.status) = 'completed';


-- 4. Report: total sales by state and month
CREATE OR REPLACE TABLE rpt_sales_by_state AS
SELECT strftime(txn_date, '%Y-%m') AS month,
       state,
       COUNT(*) AS transactions,
       SUM(amount) AS total_amount
FROM wh_transactions
GROUP BY month, state
ORDER BY month, state;
