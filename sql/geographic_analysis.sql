-- State, city, and city population analysis.

-- 1. State-level summary excluding DE
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
WHERE state <> 'DE'
GROUP BY state
ORDER BY fraud_rate_pct DESC;

-- 2. Top 15 states by transaction volume excluding DE
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
WHERE state <> 'DE'
GROUP BY state
ORDER BY total_transactions DESC
LIMIT 15;

-- 3. Top 15 states by fraud cases excluding DE
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
WHERE state <> 'DE'
GROUP BY state
ORDER BY fraud_cases DESC
LIMIT 15;

-- 4. City-level summary
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY city
ORDER BY fraud_rate_pct DESC;

-- 5. Top 20 cities by fraud rate with minimum support
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY fraud_rate_pct DESC, transaction_count DESC
LIMIT 20;

-- 6. Top 20 cities by fraud cases with minimum support
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY fraud_cases DESC, transaction_count DESC
LIMIT 20;

-- 7. Top 15 cities by transaction volume
SELECT
    city,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY city
ORDER BY transaction_count DESC
LIMIT 15;

-- 8. City population band summary
WITH city_bands AS (
    SELECT
        *,
        CASE
            WHEN city_pop <= q1 THEN 'Very Low'
            WHEN city_pop <= q2 THEN 'Low'
            WHEN city_pop <= q3 THEN 'Medium'
            WHEN city_pop <= q4 THEN 'High'
            ELSE 'Very High'
        END AS city_pop_band
    FROM (
        SELECT
            t.*,
            quantile_cont(city_pop, 0.2) OVER () AS q1,
            quantile_cont(city_pop, 0.4) OVER () AS q2,
            quantile_cont(city_pop, 0.6) OVER () AS q3,
            quantile_cont(city_pop, 0.8) OVER () AS q4
        FROM transactions t
    )
)
SELECT
    city_pop_band,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM city_bands
GROUP BY city_pop_band
ORDER BY
    CASE city_pop_band
        WHEN 'Very Low' THEN 1
        WHEN 'Low' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'High' THEN 4
        WHEN 'Very High' THEN 5
    END;
