CREATE DATABASE IF NOT EXISTS solagora;

CREATE EXTERNAL TABLE IF NOT EXISTS solagora.transactions_country (
  transaction_id        string,
  country_code          string,
  country               string,
  transaction_date      date,
  bank                  string,
  company               string,
  transaction_value     double,
  payment_due_date      date,
  days_delay            int,
  is_late               boolean
)
PARTITIONED BY (
  ingestion_date string
)
STORED AS PARQUET
LOCATION 's3://solagoralmb/gold/transactions_country/';

MSCK REPAIR TABLE solagora.transactions_country;
