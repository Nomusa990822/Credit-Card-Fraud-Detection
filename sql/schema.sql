-- schema.sql
-- Creates a unified transaction table schema for the credit card fraud project.

DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    trans_date_trans_time TIMESTAMP,
    cc_num BIGINT,
    merchant VARCHAR,
    category VARCHAR,
    amt DOUBLE,
    first VARCHAR,
    last VARCHAR,
    gender VARCHAR,
    street VARCHAR,
    city VARCHAR,
    state VARCHAR,
    zip BIGINT,
    lat DOUBLE,
    long DOUBLE,
    city_pop BIGINT,
    job VARCHAR,
    dob DATE,
    trans_num VARCHAR,
    unix_time BIGINT,
    merch_lat DOUBLE,
    merch_long DOUBLE,
    is_fraud INTEGER
);
