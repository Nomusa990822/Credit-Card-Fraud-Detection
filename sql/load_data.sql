-- Loads train and test CSVs into DuckDB and builds a unified transactions table.

DROP TABLE IF EXISTS train_raw;
DROP TABLE IF EXISTS test_raw;
DROP TABLE IF EXISTS transactions;

CREATE TABLE train_raw AS
SELECT * FROM read_csv_auto('data/raw/train.csv', HEADER=TRUE);

CREATE TABLE test_raw AS
SELECT * FROM read_csv_auto('data/raw/test.csv', HEADER=TRUE);

CREATE TABLE transactions AS
SELECT * FROM train_raw
UNION ALL
SELECT * FROM test_raw;
