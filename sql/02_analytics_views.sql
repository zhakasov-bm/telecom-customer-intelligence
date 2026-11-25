CREATE SCHEMA IF NOT EXISTS analytics;


CREATE OR REPLACE VIEW analytics.customer_overview AS
SELECT
    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE churn = 0
    ) AS retained_customers,

    COUNT(*) FILTER (
        WHERE churn = 1
    ) AS churned_customers,

    ROUND(
        AVG(churn::numeric) * 100,
        2
    ) AS churn_rate,

    ROUND(
        AVG(monthly_charges)::numeric,
        2
    ) AS avg_monthly_charges,

    ROUND(
        AVG(tenure)::numeric,
        2
    ) AS avg_tenure

FROM staging.customers;


CREATE OR REPLACE VIEW analytics.churn_by_contract AS
SELECT
    contract,

    COUNT(*) AS total_customers,

    SUM(churn) AS churned_customers,

    ROUND(
        AVG(churn::numeric) * 100,
        2
    ) AS churn_rate

FROM staging.customers
GROUP BY contract;


CREATE OR REPLACE VIEW analytics.churn_by_internet AS
SELECT
    internet_service,

    COUNT(*) AS total_customers,

    SUM(churn) AS churned_customers,

    ROUND(
        AVG(churn::numeric) * 100,
        2
    ) AS churn_rate

FROM staging.customers
GROUP BY internet_service;