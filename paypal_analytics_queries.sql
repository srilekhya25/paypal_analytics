CREATE DATABASE paypal_analytics;
USE paypal_analytics;


CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id VARCHAR(50),
    merchant_id VARCHAR(50),
    transaction_date DATETIME,
    amount DECIMAL(10,2),
    currency VARCHAR(10),
    country VARCHAR(10),
    payment_method VARCHAR(20),
    status VARCHAR(20),
    failure_reason VARCHAR(50)
);


select * from transactions

USE paypal_analytics;
SELECT TOP 20 * FROM [dbo].[paypal_transactions];


SELECT COUNT(*) FROM [dbo].[paypal_transactions];


WITH CTE AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY transaction_date) AS rn
    FROM paypal_transactions
)
DELETE FROM CTE WHERE rn > 1;



USE paypal_analytics;
GO

-- Drop the view if it already exists
IF OBJECT_ID('dbo.vw_paypal_transactions_summary', 'V') IS NOT NULL
    DROP VIEW dbo.vw_paypal_transactions_summary;
GO

CREATE VIEW dbo.vw_paypal_transactions_summary AS
WITH MonthlySummary AS (
    SELECT 
        FORMAT(transaction_date, 'yyyy-MM') AS Month,
        COUNT(*) AS MonthlyTransactionCount,
        SUM(amount) AS MonthlyTotalAmount
    FROM paypal_transactions
    GROUP BY FORMAT(transaction_date, 'yyyy-MM')
),
TopCustomers AS (
    SELECT TOP 10
        customer_id,
        SUM(amount) AS TotalSpent,
        COUNT(*) AS TransactionCount
    FROM paypal_transactions
    GROUP BY customer_id
    ORDER BY TotalSpent DESC
)
SELECT
    pt.transaction_id,
    pt.customer_id,
    pt.merchant_id,
    pt.transaction_date,
    pt.amount,
    pt.currency,
    pt.country,
    pt.payment_method,
    pt.status,
    pt.failure_reason,
    -- Aggregated totals
    (SELECT COUNT(*) FROM paypal_transactions) AS TotalTransactions,
    (SELECT SUM(amount) FROM paypal_transactions) AS TotalAmount,
    (SELECT AVG(amount) FROM paypal_transactions) AS AverageAmount,
    -- Monthly data
    ms.Month AS TransactionMonth,
    ms.MonthlyTransactionCount,
    ms.MonthlyTotalAmount,
    -- Top customer info
    tc.TotalSpent AS TopCustomerTotalSpent,
    tc.TransactionCount AS TopCustomerTransactionCount
FROM paypal_transactions pt
LEFT JOIN MonthlySummary ms
    ON FORMAT(pt.transaction_date, 'yyyy-MM') = ms.Month
LEFT JOIN TopCustomers tc
    ON pt.customer_id = tc.customer_id;
GO


USE paypal_analytics;
GO

----------------------------------------
-- 1?? Total number of transactions
----------------------------------------
SELECT COUNT(*) AS TotalTransactions
FROM paypal_transactions;
GO

----------------------------------------
-- 2?? Total and average amount of transactions
----------------------------------------
SELECT 
    SUM(amount) AS TotalAmount,
    AVG(amount) AS AverageAmount
FROM paypal_transactions;
GO

----------------------------------------
-- 3?? Transactions by country
----------------------------------------
SELECT 
    country,
    COUNT(*) AS TransactionCount,
    SUM(amount) AS TotalAmount
FROM paypal_transactions
GROUP BY country
ORDER BY TotalAmount DESC;
GO

----------------------------------------
-- 4?? Transactions by payment method
----------------------------------------
SELECT 
    payment_method,
    COUNT(*) AS TransactionCount,
    SUM(amount) AS TotalAmount
FROM paypal_transactions
GROUP BY payment_method
ORDER BY TotalAmount DESC;
GO

----------------------------------------
-- 5?? Transactions by status
----------------------------------------
SELECT 
    status,
    COUNT(*) AS TransactionCount,
    SUM(amount) AS TotalAmount
FROM paypal_transactions
GROUP BY status;
GO

----------------------------------------
-- 6?? Top 10 customers b
