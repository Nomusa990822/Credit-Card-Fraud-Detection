-- Amount behavior across fraud classes and general amount summaries.

-- 1. Amount summary by fraud status
SELECT
    is_fraud,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amt), 4) AS avg_amount,
    ROUND(MEDIAN(amt), 4) AS median_amount,
    ROUND(MIN(amt), 4) AS min_amount,
    ROUND(MAX(amt), 4) AS max_amount
FROM transactions
GROUP BY is_fraud
ORDER BY is_fraud;

-- 2. Overall amount summary
SELECT
    COUNT(*) AS transaction_count,
    ROUND(AVG(amt), 4) AS avg_amount,
    ROUND(MEDIAN(amt), 4) AS median_amount,
    ROUND(STDDEV_SAMP(amt), 4) AS std_amount,
    ROUND(MIN(amt), 4) AS min_amount,
    ROUND(MAX(amt), 4) AS max_amount
FROM transactions;

-- 3. Top categories by average amount
SELECT
    category,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amt), 4) AS avg_amount,
    ROUND(MEDIAN(amt), 4) AS median_amount
FROM transactions
GROUP BY category
ORDER BY avg_amount DESC;

-- 4. Amount summary by state excluding DE
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amt), 4) AS avg_amount,
    ROUND(MEDIAN(amt), 4) AS median_amount
FROM transactions
WHERE state <> 'DE'
GROUP BY state
ORDER BY avg_amount DESC;
