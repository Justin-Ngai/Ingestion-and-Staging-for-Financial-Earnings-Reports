-- Step 1: Drop the existing table to "overwrite" it
DROP TABLE IF EXISTS raw.fmp_articles_source;

-- Step 2: Create the table with the new schema and dynamic location
CREATE EXTERNAL TABLE raw.fmp_articles_source (
    title STRING,
    date STRING,
    content STRING,
    tickers STRING,
    image STRING,
    link STRING,
    author STRING,
    site STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://raw-us-east-1-jngai-dev/fmp/news_articles/${TICKER}/target/';
