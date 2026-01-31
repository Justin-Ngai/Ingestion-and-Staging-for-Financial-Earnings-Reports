CREATE TABLE equity_research.fmp_articles (
    title STRING,
    date STRING,
    content STRING,
    tickers STRING,
    image STRING,
    link STRING,
    author STRING,
    site STRING,
    ingestion_date DATE,
    last_updated TIMESTAMP
)
--LOCATION 's3://stage-us-east-1-jngai-dev/iceberg/fmp_articles/'
TBLPROPERTIES (
    'table_type' = 'ICEBERG',
    'format' = 'parquet',
    'write_compression' = 'snappy',
    'optimize_rewrite_delete_file_threshold' = '10'
);
