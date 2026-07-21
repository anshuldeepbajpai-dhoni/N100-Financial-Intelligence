### Objective

The objective of Day 15 was to build the core Financial Screener module that filters companies based on configurable financial thresholds. This module enables users to identify companies satisfying predefined investment criteria using a YAML-driven configuration.

### Tasks Completed
Developed the Financial Screener Engine.
Implemented configurable threshold-based filtering using screener_config.yaml.
Added support for minimum and maximum financial metric filters.
Integrated custom filters for Debt-to-Equity and Interest Coverage.
Renamed analytics output columns to standardized screener columns.
Implemented Composite Quality Score calculation.
Ranked screened companies based on quality score.
Integrated the screener into the main project pipeline.
Generated screened company results.

### Modules Developed
src/
└── screener/
    ├── engine.py
    ├── filters.py
    ├── scoring.py
    └── screener_config.yaml

### Features Implemented
Configurable screening thresholds
ROE filter
ROCE filter
Operating Profit Margin filter
Sales filter
Net Profit filter
Market Capitalization filter
Composite Quality Score
Automatic ranking
CSV-ready output

### Output

The screener successfully filtered companies and ranked them based on financial quality metrics.