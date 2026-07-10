# N100 Financial Intelligence Platform

A financial data engineering and analytics platform designed to ingest, normalize, validate, store, analyze, and visualize NIFTY 100 company data.

## Project Status

- Project Start Date: 05 July 2026
- Current Sprint: Sprint 1 — Data Foundation
- Current Stage: Day 3 — Data Quality Validation
- Status: Active

## Sprint 1 Goal

Build a fully loaded and validated SQLite database containing all required financial tables from the source datasets.

The Sprint 1 foundation includes:

- Excel data ingestion
- Data normalization
- Schema validation
- DQ-01 to DQ-16
- Load auditing
- SQLite schema creation
- Full data loading
- Manual quality review
- Exploratory SQL queries

## Completed Work

### Day 1 — Environment Setup

- Created the project directory structure
- Created and activated a Python virtual environment
- Installed project dependencies
- Configured environment files
- Created Makefile targets
- Initialized Git
- Created the GitHub repository
- Committed and pushed the project structure

### Day 2 — Excel Loader and Normalization

- Implemented a reusable Excel loader
- Added support for core and supplementary datasets
- Implemented data normalization
- Added column-name standardization
- Added year normalization
- Added ticker normalization
- Added structured logging
- Loaded all 12 source files
- Generated `output/load_audit.csv`

### Day 3 — Schema Validator and Data Quality

- Implemented Validator V2
- Added configuration-driven validation
- Implemented DQ-01 through DQ-16
- Added dataset-specific mandatory fields
- Added configured numeric-column validation
- Added accounting-rule tolerances
- Added severity classification
- Added validation statistics
- Generated `output/validation_failures.csv`
- Calibrated validation rules to reduce false positives
- Performed diagnostics for invalid years and duplicate keys

## Latest Validation Results

| Metric | Result |
|---|---:|
| Total validation checks | 92 |
| Passed | 71 |
| Failed | 21 |
| Critical rule failures | 16 |
| Warning rule failures | 5 |

> The failure count represents failed validation checks, not necessarily the total number of invalid records. Detailed row-level findings are recorded in the validation output and diagnostic results.

## Current Data-Quality Findings

- 100 P&L records contain missing financial years.
- 12 TCS cash-flow records contain an invalid year value of `1`.
- 26 P&L rows participate in duplicate `(company_id, year)` keys.
- 308 balance-sheet rows participate in duplicate `(company_id, year)` keys.
- 58 cash-flow rows participate in duplicate `(company_id, year)` keys.
- Several company identifiers in dependent datasets are absent from the company master dataset.

## Project Structure

```text
N100-Financial-Intelligence/
│
├── data/
│   ├── raw/
│   └── supplementary/
│
├── db/
│   └── schema.sql
│
├── notebooks/
│
├── output/
│   ├── load_audit.csv
│   └── validation_failures.csv
│
├── src/
│   └── etl/
│       ├── config.py
│       ├── loader.py
│       ├── logger.py
│       ├── normalizer.py
│       ├── validation_config.py
│       ├── validation_rules.py
│       └── validator.py
│
├── tests/
│   └── etl/
│
├── main.py
├── Makefile
├── requirements.txt
└── README.md

Data Quality Framework
Rule	Description
DQ-01	Primary-key uniqueness
DQ-02	Composite-key uniqueness
DQ-03	Foreign-key integrity
DQ-04	Duplicate-row detection
DQ-05	Mandatory-field validation
DQ-06	Positive-sales validation
DQ-07	OPM cross-check
DQ-08	Balance-sheet consistency
DQ-09	Net-cash-flow reconciliation
DQ-10	Tax-rate validation
DQ-11	Dividend-payout validation
DQ-12	EPS-sign consistency
DQ-13	URL-format validation
DQ-14	Financial-year validation
DQ-15	Numeric-field validation
DQ-16	Company-coverage validation
Generated Outputs
Load Audit
output/load_audit.csv

Contains:

dataset name,
loaded row count,
column count,
loading status,
execution time.
Validation Report
output/validation_failures.csv

Contains:

dataset,
validation rule,
severity,
failure count.
Run the Pipeline

Activate the virtual environment:

.venv\Scripts\Activate.ps1

Run the ETL and validation pipeline:

python main.py
Next Steps
Classify duplicate composite-key records.
Remove only verified exact duplicates.
Investigate missing P&L financial years.
Correct invalid TCS cash-flow years.
Reconcile missing company identifiers with the master dataset.
Re-run all validation rules.
Resolve remaining critical failures.
Begin Day 4 SQLite database schema implementation.
Sprint Progress
Day	Task	Status
Day 1	Environment Setup	Completed
Day 2	Excel Loader and Normalization	Completed
Day 3	Schema Validator and DQ Rules	In progress — remediation pending
Day 4	SQLite Database Schema	Not started
Day 5	Full Data Load	Not started
Day 6	Manual Data Review	Not started
Day 7	Sprint Review and Wrap-Up	Not started