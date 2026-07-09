# N100 Financial Intelligence Platform

## Project Overview

The **N100 Financial Intelligence Platform** is a Data Engineering and Financial Analytics project designed to build a structured financial database for NIFTY 100 companies. The platform implements a complete ETL pipeline, performs automated data quality validation, stores cleaned data in SQLite, and provides a scalable foundation for financial analytics, dashboards, APIs, and machine learning applications.

---

# Project Objectives

- Build a reusable ETL pipeline
- Load and normalize financial datasets
- Validate data using Data Quality (DQ) rules
- Store validated data in SQLite
- Perform financial analysis
- Develop interactive dashboards
- Expose data through REST APIs

---

# Tech Stack

- Python
- Pandas
- NumPy
- SQLite
- SQLAlchemy
- OpenPyXL
- Loguru
- Pytest
- Matplotlib
- Plotly
- Jupyter Notebook
- Git & GitHub

---

# Current Project Structure

```text
N100-Financial-Intelligence/
│
├── .github/
├── data/
│   ├── raw/
│   ├── processed/
│   └── supplementary/
│
├── db/
├── docs/
├── logs/
├── notebooks/
├── output/
├── reports/
├── src/
│   ├── config/
│   ├── database/
│   ├── etl/
│   └── utils/
│
├── tests/
│   └── etl/
│
├── .env
├── .gitignore
├── main.py
├── Makefile
├── README.md
└── requirements.txt
```

---

# Sprint Progress

## Sprint 1 – Data Foundation

### Day 1 – Environment Setup ✅

Completed:

- Project initialization
- GitHub repository setup
- Virtual environment configuration
- Dependency installation
- Project folder structure
- Configuration files
- Initial documentation

---

### Day 2 – Excel Loader & Data Normalization ✅

Completed:

- Generic Excel Loader
- Automatic Core/Supplementary dataset detection
- Data normalization module
- Column normalization
- Company ID normalization
- Year normalization
- Duplicate removal
- Centralized ETL logging
- Automated Load Audit generation (`load_audit.csv`)
- Successfully loaded all project datasets

---

# Modules Implemented

## ETL

- Excel Loader
- Data Normalizer
- Logger
- Configuration Manager

---

# Output Generated

```
output/
│
└── load_audit.csv
```

```
logs/
│
└── etl.log
```

---

# Upcoming Work

### Sprint 1 – Day 3

Implementation of the **Data Quality Validation Engine** including:

- DQ-01 Primary Key Validation
- DQ-02 Composite Key Validation
- DQ-03 Foreign Key Validation
- DQ-04 Balance Sheet Validation
- DQ-05 Operating Margin Validation
- DQ-06 Positive Sales Validation
- Remaining DQ-07 to DQ-16 rules
- `validation_failures.csv`

---

# Current Status

| Sprint | Day | Status |
|---------|-----|--------|
| Sprint 1 | Day 1 | ✅ Completed |
| Sprint 1 | Day 2 | ✅ Completed |
| Sprint 1 | Day 3 | ⏳ In Progress |

---

# Author

**Anshul Deep Bajpai**

B.Tech CSE (AI & ML)

N100 Financial Intelligence Platform

2026