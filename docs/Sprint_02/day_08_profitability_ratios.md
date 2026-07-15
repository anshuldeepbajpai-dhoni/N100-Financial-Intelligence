# N100 Financial Intelligence Platform

## Sprint 2 — Day 08

### Profitability Ratio Engine

---

## Project Information

| Field | Details |
|---|---|
| Project | N100 Financial Intelligence Platform |
| Sprint | Sprint 2 |
| Epic | Epic 02 — Financial Ratio Engine |
| Day | Day 08 |
| Module | Profitability Ratio Engine |
| Primary File | `src/analytics/ratios.py` |
| Test File | `tests/kpi/test_profitability_ratios.py` |
| Status | Completed Successfully |

---

## Objective

The objective of Day 08 was to develop a reusable and edge-case-safe profitability ratio engine for the N100 Financial Intelligence Platform.

The module calculates key profitability and return metrics while safely handling zero denominators, invalid inputs, negative shareholder equity, and source-data differences.

---

## Work Completed

The following components were implemented:

- Created the `FinancialRatioCalculator` class.
- Created the reusable `RatioResult` data class.
- Implemented safe numeric conversion.
- Implemented Net Profit Margin.
- Implemented Operating Profit Margin.
- Added source OPM cross-check logic.
- Added configurable OPM mismatch tolerance.
- Implemented Return on Equity.
- Implemented Return on Capital Employed.
- Implemented Return on Assets.
- Added financial-sector ROCE benchmark classification.
- Added profitability formula unit tests.
- Verified all implemented profitability calculations.

---

## Implemented Financial Ratios

### 1. Net Profit Margin

Formula:

```text
Net Profit Margin
= Net Profit / Sales × 100

Business rule:

Return None when sales is zero.
Return None when required input values are missing or invalid.
2. Operating Profit Margin

Formula:

Operating Profit Margin
= Operating Profit / Sales × 100

Business rule:

Return None when sales is zero.
Return None when required input values are missing or invalid.
3. Operating Profit Margin Cross-Check

The calculated operating margin is compared with the source opm_percentage value.

Classification:

Difference <= 1 percentage point
→ MATCH

Difference > 1 percentage point
→ OPM_MISMATCH

Missing calculated or source value
→ CROSS_CHECK_UNAVAILABLE

The result stores:

computed OPM;
source OPM;
absolute difference;
comparison flag.
4. Return on Equity

Formula:

ROE
= Net Profit
  / (Equity Capital + Reserves)
  × 100

Business rules:

Return None when shareholder equity is zero.
Return None when shareholder equity is negative.
Return None when required input values are unavailable.

This prevents misleading ROE calculations for companies with invalid or negative equity bases.

5. Return on Capital Employed

Formula:

ROCE
= EBIT
  / (
      Equity Capital
      + Reserves
      + Borrowings
    )
  × 100

Business rules:

Return None when capital employed is zero.
Return None when capital employed is negative.
Return None when required values are missing.
6. Return on Assets

Formula:

ROA
= Net Profit / Total Assets × 100

Business rules:

Return None when total assets are zero.
Return None when required values are unavailable.
Financial-Sector Handling

Companies belonging to the Financials broad sector use a sector-relative ROCE benchmark.

Financials
→ SECTOR_RELATIVE

Other sectors
→ ABSOLUTE

This decision recognizes that capital structure and leverage are structurally different for banks, NBFCs, insurers, and other financial institutions.

Unit Testing

Test file:

tests/kpi/test_profitability_ratios.py

Test coverage includes:

normal Net Profit Margin;
zero-sales Net Profit Margin;
normal Operating Profit Margin;
zero-sales Operating Profit Margin;
OPM mismatch detection;
valid OPM source match;
normal ROE;
negative-equity ROE;
normal ROCE;
normal ROA;
financial-sector ROCE benchmark;
nonfinancial-sector ROCE benchmark.
Test Result
Tests Executed : 12
Passed         : 12
Failed         : 0
Files Created or Updated
src/analytics/ratios.py

src/analytics/__init__.py

tests/kpi/__init__.py

tests/kpi/test_profitability_ratios.py
Outcome

Day 08 successfully established the profitability component of the Financial Ratio Engine.

The implementation provides reusable, tested, and edge-case-safe calculations for profitability margins, shareholder returns, capital returns, and asset returns.

Day 08 Status
Profitability Ratio Engine : COMPLETED
Unit Tests                 : 12/12 PASSED
Failed Tests               : 0
Day 08 Status              : COMPLETED SUCCESSFULLY