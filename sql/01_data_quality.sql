-- Total number of records
SELECT COUNT(*) AS total_records
FROM raw.customers;


-- Duplicate customer IDs
SELECT
    "customerID",
    COUNT(*) AS occurrences
FROM raw.customers
GROUP BY "customerID"
HAVING COUNT(*) > 1;


-- Missing TotalCharges
SELECT
    "customerID",
    tenure,
    "MonthlyCharges",
    "TotalCharges"
FROM raw.customers
WHERE
    "TotalCharges" IS NULL
    OR TRIM("TotalCharges") = '';


-- Invalid target values
SELECT DISTINCT "Churn"
FROM raw.customers
WHERE
    "Churn" IS NULL
    OR "Churn" NOT IN ('Yes', 'No');


-- Target distribution
SELECT
    "Churn",
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM raw.customers
GROUP BY "Churn";