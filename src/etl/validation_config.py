"""
Validation Configuration
Sprint 1 - Day 3
"""

DATASET_CONFIG = {

    "companies.xlsx": {
        "primary_key": "id",
        "mandatory": [
            "id",
            "company_name"
        ]
    },

    "profitandloss.xlsx": {
        "primary_key": "id",
        "validate_year": True,
        "numeric_columns": [
        "sales",
        "expenses",
        "operating_profit",
        "other_income",
        "interest",
        "depreciation",
        "profit_before_tax",
        "tax_percentage",
        "net_profit",
        "eps",
        "dividend_payout"
        ],
        "composite_key": [
            "company_id",
            "year"
        ],
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id",
            "year",
            "sales",
            "operating_profit",
            "net_profit"
        ]
    },

    "balancesheet.xlsx": {
        "primary_key": "id",
        "validate_year": True,
        "numeric_columns":[
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
        "total_liabilities",
        "fixed_assets",
        "cwip",
        "investments",
        "other_asset",
        "total_assets"
        ],
        "composite_key": [
            "company_id",
            "year"
        ],
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id",
            "year",
            "total_assets",
            "total_liabilities"
        ]
    },

    "cashflow.xlsx": {
        "primary_key": "id",
        "validate_year": True,
        "numeric_columns":[
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
        ],
        "composite_key": [
            "company_id",
            "year"
        ],
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id",
            "year",
            "net_cash_flow"
        ]
    },

    "analysis.xlsx": {
        "primary_key": "id",
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id"
        ]
    },

    "documents.xlsx": {
        "primary_key": "id",
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id"
        ]
    },

    "prosandcons.xlsx": {
        "primary_key": "id",
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id"
        ]
    },

    "financial_ratios.xlsx": {
        "primary_key": "id",
        "validate_year": True,
        "numeric_columns":[
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr"
        ],
        "foreign_key": {
            "column": "company_id",
            "master_dataset": "companies.xlsx",
            "master_key": "id"
        },
        "mandatory": [
            "company_id",
            "year",
            "earnings_per_share"
        ]
    },

    "market_cap.xlsx": {
        "primary_key": "id",
        "mandatory": [
            "company_id",
            "year"
        ]
    },

    "stock_prices.xlsx": {
        "primary_key": "id",
        "mandatory": [
            "company_id"
        ]
    },

    "peer_groups.xlsx": {
        "primary_key": "id",
        "mandatory": [
            "company_id"
        ]
    },

    "sectors.xlsx": {
        "primary_key": "id",
        "mandatory": [
            "company_id"
        ]
    }
}

TOLERANCE = {
    "balance_sheet": 0.01,
    "operating_profit": 1.0,
    "cash_flow": 0.10
}