These are the code files for an AWS architecture that ingests earnings call transcripts and news articles, then eventually upserts them into Iceberg tables. For a full description and more, see the accompanying Medium article: https://medium.com/p/261c44edd20a/edit

The intent of code in each folder is:
- Ingestion-layer: getting from data sources the financial texts
- Staging-layer: creating a table for each type of text, upserting into these tables
- Orchestration: calling services to do the above
