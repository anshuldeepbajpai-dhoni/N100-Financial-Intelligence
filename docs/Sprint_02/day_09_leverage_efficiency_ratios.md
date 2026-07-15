# N100 Financial Intelligence Platform

## Sprint 2 — Day 09

### Leverage and Efficiency Ratio Engine

---

## Project Information

| Field | Details |
|---|---|
| Project | N100 Financial Intelligence Platform |
| Sprint | Sprint 2 |
| Epic | Epic 02 — Financial Ratio Engine |
| Day | Day 09 |
| Module | Leverage and Efficiency Ratios |
| Primary File | `src/analytics/ratios.py` |
| Test File | `tests/kpi/test_leverage_efficiency_ratios.py` |
| Status | Completed Successfully |

---

## Objective

The objective of Day 09 was to extend the Financial Ratio Engine with leverage, debt-servicing, liquidity-proxy, and operating-efficiency metrics.

The implementation handles debt-free companies, negative shareholder equity, high financial-sector leverage, low interest coverage, negative net debt, and zero-asset edge cases.

---

## Work Completed

The following features were implemented:

- Implemented Debt-to-Equity ratio.
- Added debt-free company handling.
- Added negative-equity protection.
- Implemented high-leverage risk classification.
- Added financial-sector high-leverage suppression.
- Implemented Interest Coverage Ratio.
- Added the `Debt Free` ICR display label.
- Added ICR risk-warning logic.
- Implemented Net Debt.
- Preserved valid negative net-debt values.
- Implemented Asset Turnover.
- Added leverage and efficiency unit tests.
- Verified all Day 09 formulas and edge cases.

---

## Implemented Financial Ratios

### 1. Debt-to-Equity Ratio

Formula:

```text
Debt-to-Equity
= Borrowings
  / (Equity Capital + Reserves)

Business rules:

Borrowings = 0
→ Return 0.0

Shareholder Equity <= 0
→ Return None

Missing or invalid inputs
→ Return None

Returning 0.0 for debt-free companies distinguishes a valid zero-debt capital structure from a missing or uncomputable ratio.

2. High-Leverage Flag

Rule:

Debt-to-Equity > 5
AND
Broad Sector != Financials

→ high_leverage_flag = True

Financial-sector companies are excluded because structurally high leverage is common in banking, insurance, lending, and other financial businesses.

3. Interest Coverage Ratio

Formula:

Interest Coverage Ratio
= (
    Operating Profit
    + Other Income
  )
  / Interest

Business rules:

Interest = 0
→ Return None

Missing required values
→ Return None

A zero-interest company is treated as debt-free for display purposes.

4. Interest-Coverage Label

Classification:

Interest = 0
→ Debt Free

ICR is unavailable for another reason
→ Not Available

ICR < 1.5
→ At Risk

ICR >= 1.5
→ Covered
5. Interest-Coverage Warning

Rule:

ICR < 1.5
→ Warning = True

ICR >= 1.5
→ Warning = False

ICR is None
→ Warning = False

Debt-free companies are handled separately and are not incorrectly classified as high-risk companies.

6. Net Debt

Formula:

Net Debt
= Borrowings - Investments

Investments are used as a liquid-asset proxy.

Negative net debt is retained because it indicates that liquid investments exceed total borrowings.

7. Asset Turnover

Formula:

Asset Turnover
= Sales / Total Assets

Business rules:

Return None when total assets are zero.
Return None when required values are unavailable.
Financial-Sector Carve-Out

The standard high-leverage warning is suppressed for:

broad_sector = Financials

This treatment prevents banks, NBFCs, insurers, and other financial institutions from being incorrectly flagged under a capital-structure rule intended for nonfinancial companies.

Unit Testing

Test file:

tests/kpi/test_leverage_efficiency_ratios.py

Test coverage includes:

normal Debt-to-Equity;
debt-free D/E equals zero;
negative-equity D/E;
high leverage for a nonfinancial company;
financial-sector leverage suppression;
normal Interest Coverage Ratio;
zero-interest ICR;
debt-free ICR label;
low-ICR warning;
healthy-ICR classification;
normal Net Debt;
negative Net Debt;
normal Asset Turnover;
zero-assets Asset Turnover.
Test Result
Tests Executed : 14
Passed         : 14
Failed         : 0
Files Created or Updated
src/analytics/ratios.py

tests/kpi/test_leverage_efficiency_ratios.py
Outcome

Day 09 successfully extended the Financial Ratio Engine with leverage, debt-servicing, liquidity-proxy, and efficiency calculations.

The implementation safely distinguishes debt-free companies from missing data and applies appropriate sector-specific leverage rules.

Day 09 Status
Leverage Ratio Engine   : COMPLETED
Efficiency Ratio Engine : COMPLETED
Unit Tests              : 14/14 PASSED
Failed Tests            : 0
Day 09 Status           : COMPLETED SUCCESSFULLY