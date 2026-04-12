-- Gender, age-band, and job-level summaries.

-- 1. Gender summary
SELECT
    gender,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY gender
ORDER BY gender;

-- 2. Age band summary
WITH base AS (
    SELECT
        *,
        DATE_DIFF('day', CAST(dob AS DATE), CAST(trans_date_trans_time AS DATE)) / 365.25 AS age
    FROM transactions
),
age_bands AS (
    SELECT
        *,
        CASE
            WHEN age < 25 THEN 'Under 25'
            WHEN age >= 25 AND age < 35 THEN '25-34'
            WHEN age >= 35 AND age < 45 THEN '35-44'
            WHEN age >= 45 AND age < 55 THEN '45-54'
            WHEN age >= 55 AND age < 65 THEN '55-64'
            ELSE '65+'
        END AS age_band
    FROM base
)
SELECT
    age_band,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM age_bands
GROUP BY age_band
ORDER BY
    CASE age_band
        WHEN 'Under 25' THEN 1
        WHEN '25-34' THEN 2
        WHEN '35-44' THEN 3
        WHEN '45-54' THEN 4
        WHEN '55-64' THEN 5
        WHEN '65+' THEN 6
    END;

-- 3. Exact age summary
WITH base AS (
    SELECT
        *,
        CAST(FLOOR(DATE_DIFF('day', CAST(dob AS DATE), CAST(trans_date_trans_time AS DATE)) / 365.25) AS INTEGER) AS age
    FROM transactions
)
SELECT
    age,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM base
WHERE age IS NOT NULL
GROUP BY age
ORDER BY age;

-- 4. Job-level fraud summary with minimum support
SELECT
    job,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(AVG(is_fraud), 6) AS fraud_rate,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY job
HAVING COUNT(*) >= 100
ORDER BY fraud_rate_pct DESC, transaction_count DESC
LIMIT 20;

-- 5. Top jobs by fraud cases with minimum support
SELECT
    job,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * AVG(is_fraud), 4) AS fraud_rate_pct
FROM transactions
GROUP BY job
HAVING COUNT(*) >= 100
ORDER BY fraud_cases DESC, transaction_count DESC
LIMIT 20;
