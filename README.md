# N100 Financial Intelligence Platform

## Sprint 1 — Data Foundation

The **N100 Financial Intelligence Platform** is a modular financial data-engineering and analytics system designed to transform raw company, financial-statement, market, sector, and fundamental datasets into a validated, standardized, database-driven, and analytics-ready intelligence layer.

Sprint 1 implements the complete data foundation, including data loading, normalization, validation, processed-data export, SQLite integration, database optimization, analytical SQL views, financial queries, and automated audit reporting.

---

## Sprint Status

| Day | Module | Status |
|---|---|---|
| Day 1 | Project Foundation and Dataset Configuration | Completed |
| Day 2 | ETL Loader and Load Audit | Completed |
| Day 3 | Data Normalization and Quality Validation | Completed |
| Day 4 | Processed Data Export | Completed |
| Day 5 | SQLite Database Integration | Completed |
| Day 6 | Database Integrity, Indexes and SQL Views | Completed |
| Day 7 | Financial Analytics and Final Integration | Completed |

**Overall Sprint 1 Status: Completed Successfully**

---

## Features

- Automated Excel dataset loading
- Centralized dataset configuration
- Column-name normalization
- Company-identifier normalization
- Financial-year normalization
- Data-quality validation
- Missing-value detection
- Invalid-year detection
- Duplicate classification
- Conflicting-record analysis
- Safe data cleaning
- Processed CSV export
- SQLite database creation
- Automated database loading
- Database-integrity validation
- Database table summaries
- Database index optimization
- Analytical SQL views
- Secure read-only SQL execution
- Predefined financial analytics
- Automated analytics CSV exports
- Query execution auditing
- Export manifest generation
- Modular pipeline architecture

---

## Dataset Coverage

### Core Datasets

- `companies.xlsx`
- `profitandloss.xlsx`
- `balancesheet.xlsx`
- `cashflow.xlsx`
- `analysis.xlsx`
- `documents.xlsx`
- `prosandcons.xlsx`

### Supplementary Datasets

- `sectors.xlsx`
- `stock_prices.xlsx`
- `market_cap.xlsx`
- `financial_ratios.xlsx`
- `peer_groups.xlsx`


## Known Data Quality Issues
The Sprint 1 Day 3 validation process identified several unresolved
source-level data-quality issues.

The remaining issues include:

- 176 conflicting balance-sheet records
- 22 conflicting cash-flow records
- 22 conflicting financial-ratio records
- Missing company references in the company master dataset
- Missing values in selected financial fields
- 99 non-annual or TTM profit-and-loss records without a normalized year

Exact duplicate records were removed automatically. However, records
containing conflicting financial values were intentionally preserved
to prevent accidental loss or corruption of source data.

These issues have been documented in the generated audit reports and
will be addressed during a future data-remediation iteration.

The unresolved records do not block the continuation of Sprint 1
because the ETL pipeline successfully loads, normalizes, validates,
audits, and reports all datasets.

## Current Data-Quality Findings

- 100 P&L records contain missing financial years.
- 12 TCS cash-flow records contain an invalid year value of `1`.
- 26 P&L rows participate in duplicate `(company_id, year)` keys.
- 308 balance-sheet rows participate in duplicate `(company_id, year)` keys.
- 58 cash-flow rows participate in duplicate `(company_id, year)` keys.
- Several company identifiers in dependent datasets are absent from the company master dataset.

### Day 4: Processed Data Export

Sprint 1 Day 4 focused on building a structured processed-data
layer for the N100 Financial Intelligence Platform.

### Implemented Features

- Created a reusable processed-data exporter
- Exported normalized datasets from DataFrames to CSV
- Generated 12 processed dataset files
- Added automatic post-export row-count verification
- Added export exception handling and status tracking
- Recorded row counts, column counts, file sizes, and export duration
- Generated a centralized processed-data manifest
- Preserved unresolved financial conflicts for future reconciliation
- Protected the original raw Excel datasets from modification

### Processed Data Location

```text
data/processed/

Generated Manifest

output/processed_data_manifest.csv

## Project Structure
=======
## System Architecture
>>>>>>> 8ff276d (Complete Sprint 1 data foundation and financial analytics pipeline)

```text
Raw Excel Datasets
        ↓
Excel ETL Loader
        ↓
Data Normalization
        ↓
Data-Quality Validation
        ↓
Safe Data Cleaning
        ↓
Processed CSV Export
        ↓
SQLite Database
        ↓
Database Integrity Validation
        ↓
Database Index Optimization
        ↓
Analytical SQL Views
        ↓
Financial Analytics Queries
        ↓
Analytics CSV Exports
        ↓
Audit Reports and Manifests
Project Structure
N100-Financial-Intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── n100_financial.db
│
├── docs/
│
├── output/
│   ├── analytics/
│   ├── load_audit.csv
│   ├── validation_failures.csv
│   ├── processed_data_manifest.csv
│   ├── database_load_audit.csv
│   ├── database_integrity_report.csv
│   ├── database_table_summary.csv
│   ├── database_index_audit.csv
│   ├── sql_view_validation.csv
│   ├── analytical_query_audit.csv
│   └── analytics_export_manifest.csv
│
├── src/
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── query_engine.py
│   │   ├── financial_queries.py
│   │   └── analytics_runner.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── database_loader.py
│   │   ├── integrity_checker.py
│   │   ├── indexes.py
│   │   └── views.py
│   │
│   └── etl/
│       ├── config.py
│       ├── loader.py
│       ├── normalizer.py
│       ├── validator.py
│       ├── exporter.py
│       └── logger.py
│
├── main.py
├── requirements.txt
└── README.md
Financial-Year Normalization

The normalization system converts financial-period labels into standardized integer years.

Source Value	Normalized Value
Mar 2024	2024
Dec 2012	2012
Mar-24	2024
FY24	2024
FY2024	2024
Mar 2023 15	2023
Mar 2016 9m	2016
TTM	Missing
Financial Analytics

The analytical layer executes the following queries:

Top companies by market capitalization
Highest ROE companies
Highest ROCE companies
Latest profitability ranking
Highest operating-margin companies
Annual profitability trends
Balance-sheet leverage
Cash-flow performance
Sector-wise company distribution
Complete company financial snapshot
Analytics Result
Total Queries      : 10
Successful Queries : 10
Failed Queries     : 0
Run the Project
Create a virtual environment
python -m venv .venv
Activate the environment
.venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Execute the pipeline
python main.py
Technology Stack
Python
Pandas
OpenPyXL
SQLite
SQL
Loguru
Pathlib
Git
GitHub
Sprint 1 Outcome

Sprint 1 successfully created an automated financial-data foundation capable of:

loading source financial datasets;
normalizing inconsistent data;
validating data quality;
preserving conflicting source records;
exporting standardized datasets;
creating an optimized SQLite database;
generating analytical SQL views;
executing financial analytics;
exporting query results;
generating audit reports and manifests.

The platform is ready for future dashboard development, financial scoring, forecasting, company comparisons, APIs, and machine-learning applications.

Author

Anshul Deep Bajpai

N100 Financial Intelligence Platform
Sprint 1 — Data Foundation