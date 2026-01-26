**Financial Text Ingestion and Staging Pipeline**

---

**Overview**

This repository contains an AWS-based pipeline for ingesting, staging, and structuring financial text data from Alpha Vantage and Financial Modeling Prep. The system automates the collection of earnings transcripts and news articles and loads them into Apache Iceberg tables for analytics.

---

**Architecture**

The pipeline uses AWS managed services and follows a layered design with Bronze and Silver stages.

**Scheduling (EventBridge)**

- Earnings transcripts are scheduled quarterly
- News articles are scheduled daily at 7:00 AM
- Each schedule triggers a Step Functions workflow
- Workflows receive a list of stock tickers

**Ingestion – Bronze Layer**

- Earnings transcripts collected quarterly from Alpha Vantage
- News articles collected daily from Financial Modeling Prep
- AWS Lambda fetches data and stores JSON in S3

**Orchestration (Step Functions)**

- Loops over tickers and reporting periods
- For each iteration:
  - Run ingestion Lambda
  - Store JSON in S3
  - Create Athena tables
  - Upsert into Iceberg

**Staging – Silver Layer**

- Athena external tables on raw JSON
- Data transformed and merged into Iceberg

**Analytical Storage (Iceberg)**

- Stored in S3
- Supports incremental upserts and analytics

---

**Data Layers**

| Layer  | Purpose           | Components                        |
|--------|-------------------|-----------------------------------|
| Bronze | Raw ingestion     | EventBridge, Lambda, S3 (JSON)     |
| Silver | Staging and merge | Athena, Iceberg                   |

---

**Scheduling**

| Dataset              | Frequency   | Trigger                         |
|----------------------|-------------|---------------------------------|
| Earnings Transcripts | Quarterly   | EventBridge → Step Functions    |
| News Articles        | Daily 7 AM  | EventBridge → Step Functions    |

Both pipelines follow the same orchestration pattern.

---

**Folder Structure**

The repository is organized into four main folders based on pipeline responsibilities.

**raw_processing**  
Contains all logic related to Bronze layer ingestion. This includes Lambda functions and scripts for fetching earnings transcripts and news articles and storing raw JSON in S3.

**staging_processing**  
Contains transformation and merge logic for the Silver layer. This includes Athena queries and scripts used to process raw data and prepare it for Iceberg upserts.

**orchestration**  
Contains Step Functions workflows and related configuration. This layer coordinates all services that handle files and processes defined in the processing folders.

**environment_setup**  
Contains infrastructure and setup scripts. This includes creating Apache Iceberg tables, defining schemas, and configuring resources needed for upsert operations.

---

**Repository Contents**

1. Lambda – Earnings Transcript Ingestion  
   Located in raw_processing. Fetches transcripts from Alpha Vantage and stores results in S3 as JSON.

2. Lambda – News Article Ingestion  
   Located in raw_processing. Fetches news from Financial Modeling Prep and writes normalized JSON to S3.

3. Athena – Create Iceberg Table  
   Located in environment_setup. Creates Apache Iceberg tables in S3 and defines schemas and properties.

4. Athena – Create External JSON Table  
   Located in staging_processing. Creates Athena tables over raw JSON files.

5. Athena – Upsert into Iceberg  
   Located in staging_processing. Merges staged data into Iceberg tables and handles inserts and updates.

6. Step Functions Workflow  
   Located in orchestration. JSON state machine definitions that orchestrate ingestion and transformation.

**Workflow Steps**

1. Receive parameters  
2. Invoke Lambda  
3. Create Athena tables  
4. Run Iceberg upsert

---

**Summary**

This project provides a scalable, serverless pipeline for financial text data. It separates raw ingestion from structured storage, supports automated scheduling, and enables reliable analytics using Apache Iceberg.
