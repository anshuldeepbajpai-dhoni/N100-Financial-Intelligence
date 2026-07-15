"""
Project Configuration
"""

from pathlib import Path

# ==============================
# Project Root
# ==============================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==============================
# Data Directories
# ==============================

RAW_DATA = PROJECT_ROOT / "data" / "raw"
SUPPLEMENTARY_DATA = PROJECT_ROOT / "data" / "supplementary"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

# ==============================
# Output & Logs
# ==============================

OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

PROCESSED_DATA.mkdir(
    parents=True,
    exist_ok=True
)

# ==============================
# Core Datasets
# ==============================

CORE_DATASETS = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

# ==============================
# Supplementary Datasets
# ==============================

SUPPLEMENTARY_DATASETS = [
    "sectors.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx"
]

# ==============================
# All Datasets
# ==============================

ALL_DATASETS = CORE_DATASETS + SUPPLEMENTARY_DATASETS

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = (
    DATABASE_DIR
    / "n100_financial.db"
)