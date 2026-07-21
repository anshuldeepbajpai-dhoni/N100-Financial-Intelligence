# N100 Financial Intelligence Platform

## Sprint 1, Sprint 2 & Sprint 3 — End-to-End Financial Intelligence Platform

The **N100 Financial Intelligence Platform** is a modular financial data-engineering and analytics system designed to transform raw company, financial-statement, market, sector, and fundamental datasets into a validated, standardized, database-driven, and analytics-ready intelligence layer.

The platform now includes the complete implementation of Sprint 1 (Days 1–10) and Sprint 2 (Days 11–14), including:

- Data ingestion
- Dataset configuration
- Data normalization
- Data-quality validation
- Safe data cleaning
- Processed-data export
- SQLite database integration
- Database integrity validation
- Database optimization
- Analytical SQL views
- Financial analytics queries
- Automated analytics exports
- Audit reporting and manifest generation

---

## Project Status

| Day | Module | Status |
|---|---|---|
| Day 1 | Project Foundation and Dataset Configuration | ✅ Completed |
| Day 2 | ETL Loader and Load Audit | ✅ Completed |
| Day 3 | Data Normalization and Quality Validation | ✅ Completed |
| Day 4 | Processed Data Export | ✅ Completed |
| Day 5 | SQLite Database Integration | ✅ Completed |
| Day 6 | Database Integrity, Indexes, and SQL Views | ✅ Completed |
| Day 7 | Financial Analytics and Final Integration | ✅ Completed |
| Day 8 | Financial Analytics Execution | ✅ Completed |
| Day 9 | Financial Forecasting | ✅ Completed |
| Day 10 | Portfolio Optimization | ✅ Completed |
| Day 11 | Risk Analytics | ✅ Completed |
| Day 12 | Executive Reporting | ✅ Completed |
| Day 13 | Pipeline Integration & Deliverables | ✅ Completed |
| Day 14 | Final Project Completion | ✅ Completed |

### Overall Sprint Status

```text
Sprint 1 Status : COMPLETED SUCCESSFULLY
Sprint 2 Status : COMPLETED SUCCESSFULLY
Days Completed  : 14/14
Pipeline Status : OPERATIONAL
Project Status  : END-TO-END COMPLETED
```

---

## Sprint Goal

The objective of Sprint 1 was to establish a reliable financial-data foundation capable of:

- Loading all project datasets automatically
- Standardizing inconsistent schemas and identifiers
- Normalizing financial-period values
- Detecting data-quality threats
- Removing only safe exact duplicates
- Preserving conflicting financial records
- Exporting analytics-ready processed datasets
- Loading processed data into SQLite
- Validating database integrity
- Optimizing analytical queries
- Creating reusable financial SQL views
- Executing predefined financial analytics
- Generating traceable audit reports

---

## Key Features

### ETL and Data Processing

- Automated Excel dataset loading
- Centralized dataset configuration
- Dynamic dataset discovery
- Load-status tracking
- Row-count and column-count auditing
- Column-name normalization
- Company-identifier normalization
- Financial-year normalization
- Empty-row removal
- Safe exact-duplicate removal
- Processed CSV generation
- Automated processed-data verification

### Data-Quality Validation

- Missing-value detection
- Invalid-year detection
- Duplicate-key detection
- Exact-duplicate classification
- Conflicting-record analysis
- Company-reference validation
- Financial-value validation
- Critical-issue classification
- Warning-level classification
- Automated validation reporting

### Database Engineering

- Automated SQLite database creation
- Processed CSV-to-SQLite loading
- Database load auditing
- Table-level integrity validation
- Database row-count verification
- Primary-key validation
- Foreign-key validation
- Database index creation
- Index verification
- Analytical SQL-view creation
- SQL-view validation

### Financial Analytics

- Secure read-only SQL execution
- Predefined financial-analysis queries
- Market-capitalization rankings
- Profitability rankings
- ROE and ROCE analysis
- Operating-margin analysis
- Financial-trend analysis
- Balance-sheet leverage analysis
- Cash-flow analysis
- Sector-level company analysis
- Company financial snapshots
- Automated analytics CSV exports
- Query execution auditing
- Analytics export manifest generation

---

## Dataset Coverage

The platform processes **12 financial datasets**.

### Core Datasets

| Dataset | Description |
|---|---|
| `companies.xlsx` | Company master information and fundamental metrics |
| `profitandloss.xlsx` | Revenue, expenses, operating profit, and profitability data |
| `balancesheet.xlsx` | Assets, liabilities, equity, reserves, and borrowings |
| `cashflow.xlsx` | Operating, investing, and financing cash flows |
| `analysis.xlsx` | Company-level analytical information |
| `documents.xlsx` | Financial-document and annual-report references |
| `prosandcons.xlsx` | Company strengths and risk observations |

### Supplementary Datasets

| Dataset | Description |
|---|---|
| `sectors.xlsx` | Sector and broad-sector classifications |
| `stock_prices.xlsx` | Historical stock-market price information |
| `market_cap.xlsx` | Historical market-capitalization data |
| `financial_ratios.xlsx` | Financial performance and valuation ratios |
| `peer_groups.xlsx` | Company peer-group information |

---

## System Architecture

```text
Raw Excel Datasets
        │
        ▼
Dataset Configuration
        │
        ▼
Excel ETL Loader
        │
        ▼
Load Audit
        │
        ▼
Data Normalization
        │
        ▼
Data-Quality Validation
        │
        ▼
Safe Data Cleaning
        │
        ▼
Processed CSV Export
        │
        ▼
Processed-Data Verification
        │
        ▼
SQLite Database
        │
        ▼
Database Integrity Validation
        │
        ▼
Database Index Optimization
        │
        ▼
Analytical SQL Views
        │
        ▼
Financial Analytics Queries
        │
        ▼
Analytics CSV Exports
        │
        ▼
Audit Reports and Export Manifests
```

---

## Project Structure

```text
N100-Financial-Intelligence/
│
├── data/
│   ├── raw/
│   │   ├── companies.xlsx
│   │   ├── profitandloss.xlsx
│   │   ├── balancesheet.xlsx
│   │   ├── cashflow.xlsx
│   │   ├── analysis.xlsx
│   │   ├── documents.xlsx
│   │   ├── prosandcons.xlsx
│   │   ├── sectors.xlsx
│   │   ├── stock_prices.xlsx
│   │   ├── market_cap.xlsx
│   │   ├── financial_ratios.xlsx
│   │   └── peer_groups.xlsx
│   │
│   └── processed/
│       ├── companies.csv
│       ├── profitandloss.csv
│       ├── balancesheet.csv
│       ├── cashflow.csv
│       ├── analysis.csv
│       ├── documents.csv
│       ├── prosandcons.csv
│       ├── sectors.csv
│       ├── stock_prices.csv
│       ├── market_cap.csv
│       ├── financial_ratios.csv
│       └── peer_groups.csv
│
├── database/
│   └── n100_financial.db
│
├── docs/
│   └── sprint_01/
│
├── output/
│   ├── analytics/
│   │
│   ├── load_audit.csv
│   ├── cleaning_audit.csv
│   ├── data_threat_report.csv
│   ├── validation_failures.csv
│   ├── duplicate_analysis.csv
│   ├── reporting_period_analysis.csv
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
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── database_loader.py
│   │   ├── integrity_checker.py
│   │   ├── indexes.py
│   │   └── views.py
│   │
│   └── etl/
│       ├── __init__.py
│       ├── config.py
│       ├── loader.py
│       ├── normalizer.py
│       ├── validator.py
│       ├── exporter.py
│       └── logger.py
│
├── tests/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Financial-Year Normalization

The normalization system converts inconsistent financial-period labels into standardized nullable integer years.

| Source Value | Normalized Value |
|---|---:|
| `Mar 2024` | `2024` |
| `Dec 2012` | `2012` |
| `Mar-24` | `2024` |
| `FY24` | `2024` |
| `FY2024` | `2024` |
| `Mar 2023 15` | `2023` |
| `Mar 2016 9m` | `2016` |
| `TTM` | Missing |

Nonannual periods such as `TTM` are intentionally retained as missing normalized years rather than being assigned an inaccurate annual value.

---

## Safe Data-Cleaning Strategy

The data-cleaning layer follows a conservative financial-data preservation policy.

### Automatically Removed

- Fully empty records
- Exact duplicate records
- Duplicate records that contain identical business values

### Intentionally Preserved

- Records with the same company and year but different financial values
- Source-level financial conflicts
- Financial records requiring manual reconciliation
- Nonannual reporting periods requiring additional business context

This approach prevents automatic cleaning from causing financial-data loss or selecting an incorrect source value.

---

## Known Data-Quality Issues

Sprint 1 identified several unresolved source-level data-quality issues.

The remaining findings include:

- **176 conflicting balance-sheet records**
- **22 conflicting cash-flow records**
- **22 conflicting financial-ratio records**
- Missing company references in selected dependent datasets
- Missing values in selected financial fields
- Nonannual or `TTM` profit-and-loss records without a normalized annual year
- Selected company identifiers absent from the company master dataset

Exact duplicate records were removed automatically. Records containing different financial values were intentionally preserved to prevent accidental loss or corruption of source data.

These findings are documented in the generated data-quality reports and can be addressed during a future source-reconciliation and data-remediation iteration.

The unresolved source-level findings do not prevent the platform from loading, normalizing, validating, auditing, exporting, storing, and analyzing the available datasets.

---

## Data-Quality Audit Outputs

The pipeline generates the following audit files:

| Report | Purpose |
|---|---|
| `load_audit.csv` | Records dataset loading status, rows, and columns |
| `cleaning_audit.csv` | Records safe-cleaning activity |
| `data_threat_report.csv` | Reports detected data threats |
| `validation_failures.csv` | Stores failed validation rules |
| `duplicate_analysis.csv` | Classifies duplicate records |
| `reporting_period_analysis.csv` | Analyzes reporting-period conflicts |
| `processed_data_manifest.csv` | Records processed-data export information |

---

## Processed Data Export

Sprint 1 Day 4 created a structured processed-data layer.

### Implemented Features

- Reusable processed-data exporter
- DataFrame-to-CSV export
- Export of all 12 normalized datasets
- Automatic post-export row-count verification
- Export exception handling
- Export status tracking
- Row-count recording
- Column-count recording
- File-size recording
- Export-duration tracking
- Centralized processed-data manifest
- Original raw-data protection

### Processed Data Location

```text
data/processed/
```

### Processed Data Manifest

```text
output/processed_data_manifest.csv
```

---

## SQLite Database Integration

Sprint 1 Day 5 introduced the database layer.

### Database Features

- Automated SQLite database creation
- Automated processed CSV loading
- Dynamic table creation
- Database transaction management
- Table replacement during controlled pipeline execution
- Database load auditing
- Row-count verification
- Table-level status tracking

### Database Location

```text
database/n100_financial.db
```

---

## Database Integrity and Optimization

Sprint 1 Day 6 implemented database validation and performance optimization.

### Implemented Features

- Database table discovery
- Table row-count verification
- Empty-table detection
- Schema inspection
- Database-integrity reporting
- Index creation
- Index-existence validation
- Analytical SQL-view creation
- SQL-view validation

Indexes improve filtering, joining, grouping, and company-year financial analysis.

---

## Financial Analytics

Sprint 1 Day 7 introduced the financial analytics layer.

The analytical engine executes the following predefined analyses:

1. Top companies by market capitalization
2. Highest Return on Equity companies
3. Highest Return on Capital Employed companies
4. Latest profitability rankings
5. Highest operating-margin companies
6. Annual profitability trends
7. Balance-sheet leverage analysis
8. Cash-flow performance analysis
9. Sector-wise company distribution
10. Complete company financial snapshots

---

## Analytics Execution Result

```text
Total Queries      : 10
Successful Queries : 10
Failed Queries     : 0
Success Rate       : 100%
```

---

## Analytics Outputs

Financial-analysis results are exported to:

```text
output/analytics/
```

The platform also generates:

```text
output/analytical_query_audit.csv

output/analytics_export_manifest.csv
```

These reports provide query-level traceability and analytics-export metadata.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and pipeline development |
| Pandas | Data loading, cleaning, transformation, and analysis |
| OpenPyXL | Excel workbook processing |
| SQLite | Relational financial-data storage |
| SQL | Financial querying, aggregation, and analytical views |
| Loguru | Structured pipeline logging |
| Pathlib | Cross-platform file and directory management |
| Pytest | Automated testing |
| Git | Source-code version control |
| GitHub | Repository hosting and collaboration |

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd N100-Financial-Intelligence
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

For Linux or macOS:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Complete Pipeline

Execute:

```bash
python main.py
```

The pipeline performs:

```text
Dataset Loading
        ↓
Data Normalization
        ↓
Data-Quality Validation
        ↓
Safe Data Cleaning
        ↓
Processed CSV Export
        ↓
SQLite Database Loading
        ↓
Database Integrity Validation
        ↓
Database Optimization
        ↓
SQL-View Creation
        ↓
Financial Analytics
        ↓
Analytics Export
        ↓
Audit Report Generation
```

---

## Generated Deliverables

### Data Deliverables

- 12 processed CSV datasets
- SQLite financial database
- Financial analytics CSV outputs

### Audit Deliverables

- Load audit
- Cleaning audit
- Data-threat report
- Validation-failure report
- Duplicate-analysis report
- Reporting-period analysis
- Processed-data manifest
- Database-load audit
- Database-integrity report
- Database-table summary
- Database-index audit
- SQL-view validation report
- Analytical-query audit
- Analytics export manifest

### Technical Deliverables

- Modular ETL layer
- Data-normalization engine
- Data-quality validation engine
- Processed-data exporter
- SQLite database layer
- Database integrity checker
- Database index manager
- Analytical SQL views
- Secure query engine
- Financial-query library
- Automated analytics runner

---

## Sprint 1 Outcome

Sprint 1 successfully created an automated financial-data foundation capable of:

- Loading raw financial datasets
- Standardizing inconsistent schemas
- Normalizing company identifiers
- Normalizing financial-period values
- Detecting data-quality threats
- Preserving unresolved financial conflicts
- Exporting analytics-ready datasets
- Creating a structured SQLite database
- Validating database integrity
- Optimizing database performance
- Creating reusable analytical SQL views
- Executing financial-analysis queries
- Exporting analytics results
- Generating traceable audit reports and manifests

The platform is ready for future development in:

- Financial ratio engineering
- Financial scoring
- Company screening
- Peer comparison
- Interactive dashboards
- Forecasting
- Risk analytics
- REST API development
- Machine-learning applications

---

## Future Scope

Planned enhancements include:

- Advanced financial-ratio calculations
- Multi-year CAGR analysis
- Composite company-quality scoring
- Automated financial screening
- Sector-relative benchmarking
- Company peer comparison
- Financial-health scoring
- Interactive dashboard development
- API-based analytics access
- Forecasting models
- Anomaly detection
- Machine-learning-based company classification

---

## Author

**Anshul Deep Bajpai**

B.Tech — Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning

---

## Project

**N100 Financial Intelligence Platform**

**Sprint 1 & Sprint 2 — Completed**

```text
Sprint 1      : COMPLETED
Sprint 2      : COMPLETED
Days          : 14/14 COMPLETED
Analytics     : 10/10 SUCCESSFUL
Pipeline      : OPERATIONAL
```

---

# Sprint 3 (Days 15–17)

## Overview

Sprint 3 introduces intelligent financial screening and benchmarking capabilities. Three major modules were developed:

- Financial Screener
- Preset Stock Screeners
- Peer Comparison Engine

## Day 15 – Financial Screener

- Configurable threshold-based screening
- YAML configuration
- ROE, ROCE, OPM, Sales and Market Cap filters
- Composite Quality Score
- Ranked company output

## Day 16 – Preset Stock Screeners

Implemented:

- Quality Screener
- Growth Screener
- Value Screener
- Large Cap Screener
- Dividend Screener

Features:

- One-click execution
- Automatic CSV generation
- Batch execution

## Day 17 – Peer Comparison Engine

Implemented:

- Sector-wise benchmarking
- Financial rankings
- ROE, ROCE, OPM comparison
- Net Profit comparison
- Market Capitalization comparison
- CSV export

## New Modules

```text
src/
├── screener/
│   ├── engine.py
│   ├── filters.py
│   ├── scoring.py
│   ├── presets.py
│   ├── export.py
│   └── screener_config.yaml
└── peer/
    ├── engine.py
    ├── ranking.py
    ├── export.py
    └── peer_runner.py
```

## Deliverables

- quality_screener.csv
- growth_screener.csv
- value_screener.csv
- large_cap_screener.csv
- dividend_screener.csv
- peer_comparison.csv
- peer_rankings.csv
- peer_summary.csv

## Status

Sprint 1 : COMPLETED
Sprint 2 : COMPLETED
Sprint 3 (Days 15–17) : COMPLETED
Pipeline : OPERATIONAL
