-- Fraud vs legitimate distribution.

SELECT
    is_fraud,
    COUNT(*) AS transaction_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 4) AS percentage
FROM transactions
GROUP BY is_fraud
ORDER BY is_fraud;
