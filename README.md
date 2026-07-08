# N100 Financial Intelligence Platform

## Sprint 1 – Day 1: Environment Setup

### Project Overview

The **N100 Financial Intelligence Platform** is a comprehensive data engineering and financial analytics project designed to build a structured financial database for NIFTY 100 companies. The platform will integrate multiple financial datasets, perform automated ETL (Extract, Transform, Load) operations, validate data quality, and prepare the foundation for advanced analytics, dashboards, APIs, and machine learning applications.

---

## Sprint Goal

Establish a production-ready development environment and project structure that will support the complete ETL pipeline throughout Sprint 1.

---

## Day 1 Objectives

* Set up the Python development environment.
* Create and activate a virtual environment.
* Initialize Git version control.
* Create the GitHub repository.
* Organize the project directory structure.
* Configure project files (.env, .gitignore, requirements.txt).
* Install required Python libraries.
* Prepare the repository for collaborative development.

---

## Project Structure

```
N100-Financial-Intelligence/
│
├── data/
├── db/
├── docs/
├── notebooks/
├── output/
├── reports/
├── src/
│   ├── etl/
│   ├── utils/
│   ├── config/
│   └── api/
├── tests/
├── .env
├── .gitignore
├── Makefile
├── requirements.txt
├── README.md
└── main.py
```

---

## Technologies Used

* Python
* Git & GitHub
* Visual Studio Code
* Virtual Environment (venv)
* SQLite (planned)
* Pandas
* NumPy
* SQLAlchemy
* Pytest
* Loguru
* Rich
* Plotly
* Jupyter Notebook

---

## Day 1 Deliverables

* Project repository created
* Virtual environment configured
* Required dependencies installed
* Git initialized and connected to GitHub
* Initial project structure established
* Configuration files created
* Initial project commit pushed successfully

---

## Next Steps

Sprint 1 – Day 2 will focus on implementing the ETL framework, including the Excel Loader, Data Normalization module, and unit testing for normalization functions.
