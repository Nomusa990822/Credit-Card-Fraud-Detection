-- Category summaries and category-by-gender interaction.

-- 1. Category-level fraud summary
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY category
ORDER BY fraud_rate_pct DESC;

-- 2. Top categories by transaction volume
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY category
ORDER BY transaction_count DESC;

-- 3. Category by gender fraud summary
SELECT
    gender,
    category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY gender, category
ORDER BY category, gender;
