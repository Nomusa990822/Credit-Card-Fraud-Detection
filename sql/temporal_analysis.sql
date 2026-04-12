-- Fraud patterns across hour, day, month, and night/day.

-- 1. Fraud by hour of day
SELECT
    EXTRACT(HOUR FROM trans_date_trans_time) AS trans_hour,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY trans_hour
ORDER BY trans_hour;

-- 2. Fraud by day of week
SELECT
    CASE EXTRACT(DOW FROM trans_date_trans_time)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS trans_day_name,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY EXTRACT(DOW FROM trans_date_trans_time)
ORDER BY EXTRACT(DOW FROM trans_date_trans_time);

-- 3. Fraud by month
SELECT
    EXTRACT(MONTH FROM trans_date_trans_time) AS trans_month,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY trans_month
ORDER BY trans_month;

-- 4. Fraud by night vs day
SELECT
    CASE
        WHEN EXTRACT(HOUR FROM trans_date_trans_time) >= 22
          OR EXTRACT(HOUR FROM trans_date_trans_time) <= 3
        THEN 1 ELSE 0
    END AS is_night_transaction,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY is_night_transaction
ORDER BY is_night_transaction;
