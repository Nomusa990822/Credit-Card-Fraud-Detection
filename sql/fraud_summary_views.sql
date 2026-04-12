-- Reusable views for downstream analytics and feature support.

DROP VIEW IF EXISTS vw_target_distribution;
DROP VIEW IF EXISTS vw_state_fraud_summary;
DROP VIEW IF EXISTS vw_city_fraud_summary;
DROP VIEW IF EXISTS vw_category_fraud_summary;
DROP VIEW IF EXISTS vw_merchant_fraud_summary;
DROP VIEW IF EXISTS vw_hourly_fraud_summary;

CREATE VIEW vw_target_distribution AS
SELECT
    is_fraud,
    COUNT(*) AS transaction_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS percentage
FROM transactions
GROUP BY is_fraud;

CREATE VIEW vw_state_fraud_summary AS
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
WHERE state <> 'DE'
GROUP BY state;

CREATE VIEW vw_city_fraud_summary AS
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY city;

CREATE VIEW vw_category_fraud_summary AS
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY category;

CREATE VIEW vw_merchant_fraud_summary AS
SELECT
    merchant,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY merchant;

CREATE VIEW vw_hourly_fraud_summary AS
SELECT
    EXTRACT(HOUR FROM trans_date_trans_time) AS trans_hour,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY trans_hour;
