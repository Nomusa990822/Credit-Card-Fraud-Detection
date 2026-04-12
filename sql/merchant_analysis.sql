-- Merchant-level transaction concentration and risk summaries.

-- 1. Merchant summary
SELECT
    merchant,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY merchant;

-- 2. Top 15 merchants by transaction volume
SELECT
    merchant,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY merchant
ORDER BY transaction_count DESC
LIMIT 15;

-- 3. Top 20 merchants by fraud rate with minimum support
SELECT
    merchant,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY merchant
HAVING COUNT(*) >= 100
ORDER BY fraud_rate_pct DESC, transaction_count DESC
LIMIT 20;

-- 4. Top 20 merchants by fraud cases with minimum support
SELECT
    merchant,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY merchant
HAVING COUNT(*) >= 100
ORDER BY fraud_cases DESC, transaction_count DESC
LIMIT 20;
