# N100 Financial Intelligence Platform

## Sprint 1 — Day 03  
### Schema Validator and Data Quality Framework

---

## Project Information

| Field | Details |
|---|---|
| Project Name | N100 Financial Intelligence Platform |
| Sprint | Sprint 1 — Data Foundation |
| Day | Day 03 |
| Task | Schema Validator and Data Quality Rules |
| Project Start Date | 05 July 2026 |
| Current Status | Validation Implemented — Data Remediation in Progress |
| Priority | Medium |

---

## Day 03 Objective

The objective of Sprint 1 Day 03 was to design and implement a modular, reusable, and configuration-driven data-quality validation framework for the N100 Financial Intelligence Platform.

The validation framework was developed to:

- Execute DQ-01 through DQ-16 across all applicable datasets.
- Validate primary-key and composite-key integrity.
- Verify foreign-key relationships against the company master dataset.
- Detect duplicate records.
- Validate mandatory fields.
- Perform financial and accounting consistency checks.
- Validate financial years and numeric values.
- Classify validation results as `CRITICAL` or `WARNING`.
- Generate an automated validation report.
- Identify genuine source-data issues before SQLite database loading.

---

## Work Completed

The following tasks were completed during Day 03:

- Implemented all 16 planned data-quality rules.
- Refactored the initial validator into Validator V2.
- Created a configuration-driven validation architecture.
- Added dataset-specific validation configurations.
- Added reusable validation-rule functions.
- Implemented primary-key uniqueness checks.
- Implemented `(company_id, year)` composite-key validation.
- Implemented foreign-key validation against `companies.xlsx`.
- Added duplicate-row detection.
- Added dataset-specific mandatory-field validation.
- Added positive-sales validation.
- Added operating-profit-margin cross-validation.
- Added balance-sheet consistency validation.
- Added net-cash-flow reconciliation.
- Added tax-rate validation.
- Added dividend-payout validation.
- Added EPS-sign consistency checks.
- Added URL-format validation.
- Added financial-year validation.
- Added configured numeric-column validation.
- Added company-coverage validation.
- Added configurable validation tolerances.
- Added severity-based validation results.
- Generated an automated validation report.
- Added validation statistics to the terminal output.
- Calibrated validation rules to reduce false-positive results.
- Performed manual diagnostics for invalid years and duplicate keys.

---

## Validator V2 Architecture

The original validator was refactored into a modular and configuration-driven architecture.

```text
validation_config.py
        │
        ▼
Defines dataset-specific rules,
mandatory fields, numeric columns,
and validation tolerances
        │
        ▼
validation_rules.py
        │
        ▼
Contains reusable implementations
of DQ-01 through DQ-16
        │
        ▼
validator.py
        │
        ▼
Executes configured validation rules,
classifies results, and generates reports
        │
        ▼
main.py
        │
        ▼
Runs the ETL and validation pipeline
        │
        ▼
output/validation_failures.csv