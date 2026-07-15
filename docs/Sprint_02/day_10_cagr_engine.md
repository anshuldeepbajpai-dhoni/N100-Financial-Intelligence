# N100 Financial Intelligence Platform

## Sprint 2 — Day 10

### CAGR Growth Engine

---

## Project Information

| Field | Details |
|---|---|
| Project | N100 Financial Intelligence Platform |
| Sprint | Sprint 2 |
| Epic | Epic 02 — Financial Ratio Engine |
| Day | Day 10 |
| Module | CAGR Growth Engine |
| Primary File | `src/analytics/cagr.py` |
| Test File | `tests/kpi/test_cagr.py` |
| Status | Completed Successfully |

---

## Objective

The objective of Day 10 was to develop a reusable CAGR engine for Revenue, Profit After Tax, and Earnings Per Share growth calculations.

The engine supports 3-year, 5-year, and 10-year growth windows and prevents misleading CAGR values when the underlying financial series contains losses, turnarounds, zero bases, missing values, or insufficient history.

---

## Work Completed

The following components were implemented:

- Created the `CAGRResult` data class.
- Created the reusable `CAGRCalculator`.
- Implemented the standard CAGR formula.
- Added 3-year CAGR support.
- Added 5-year CAGR support.
- Added 10-year CAGR support.
- Added historical-series CAGR calculation.
- Implemented positive-to-positive CAGR.
- Implemented positive-to-negative loss handling.
- Implemented negative-to-positive turnaround handling.
- Implemented negative-to-negative handling.
- Implemented zero-base handling.
- Implemented insufficient-history handling.
- Added invalid-input handling.
- Added positive-to-zero growth handling.
- Created comprehensive CAGR unit tests.
- Verified all CAGR edge cases.

---

## CAGR Formula

```text
CAGR
= (
    (Ending Value / Beginning Value)
    ^ (1 / Number of Years)
    - 1
  )
  × 100

Supported Growth Windows
3-Year CAGR

5-Year CAGR

10-Year CAGR

These windows can be applied to:

Revenue;
Profit After Tax;
Earnings Per Share.
Historical Observation Requirement

An n-year CAGR requires n + 1 annual observations.

Examples:

3-Year CAGR
→ 4 annual observations

5-Year CAGR
→ 6 annual observations

10-Year CAGR
→ 11 annual observations

The historical series must be ordered from the oldest value to the newest value.

CAGR Edge-Case Handling
1. Positive Beginning and Positive Ending Values

Example:

100 → 200

Action:

Calculate CAGR normally

Flag:
CALCULATED
2. Positive Beginning and Negative Ending Values

Example:

100 → -50

Action:

CAGR Value:
None

Flag:
DECLINE_TO_LOSS

A conventional CAGR is not meaningful because the company moved from profit or positive growth into a loss.

3. Negative Beginning and Positive Ending Values

Example:

-100 → 200

Action:

CAGR Value:
None

Flag:
TURNAROUND

The company experienced a financial turnaround. A standard CAGR value would be mathematically misleading.

4. Negative Beginning and Negative Ending Values

Example:

-100 → -50

Action:

CAGR Value:
None

Flag:
BOTH_NEGATIVE

A standard CAGR is not calculated when both endpoints are negative.

5. Zero Beginning Value

Example:

0 → 100

Action:

CAGR Value:
None

Flag:
ZERO_BASE

The growth rate cannot be calculated because division by zero is undefined.

6. Insufficient Historical Data

Example:

Available observations:
3

Required observations for a 5-year CAGR:
6

Action:

CAGR Value:
None

Flag:
INSUFFICIENT
Additional Edge Cases
Missing or Invalid Input
CAGR Value:
None

Flag:
INVALID_INPUT
Positive Value to Zero

Example:

100 → 0

Result:

CAGR:
-100%

Flag:
CALCULATED
CAGR Output Design

Every CAGR calculation returns:

CAGRResult

value
→ Calculated CAGR percentage or None

flag
→ Calculation status or edge-case classification

Future database columns can use the following pattern:

revenue_cagr_3yr

revenue_cagr_3yr_flag

revenue_cagr_5yr

revenue_cagr_5yr_flag

revenue_cagr_10yr

revenue_cagr_10yr_flag

The same design can be applied to PAT and EPS growth.

Unit Testing

Test file:

tests/kpi/test_cagr.py

Test coverage includes:

standard positive CAGR;
declining positive CAGR;
turnaround;
decline to loss;
both values negative;
zero base;
insufficient history;
invalid year window;
missing input;
positive value to zero;
3-year CAGR;
5-year CAGR;
10-year CAGR.
Test Result
Tests Executed : 13
Passed         : 13
Failed         : 0
Files Created or Updated
src/analytics/cagr.py

src/analytics/__init__.py

tests/kpi/test_cagr.py
Outcome

Day 10 successfully established a reusable growth-analysis engine for Revenue, PAT, and EPS.

The engine supports multiple growth windows and explicitly classifies financially meaningful edge cases rather than producing mathematically misleading CAGR values.

Day 10 Status
CAGR Engine          : COMPLETED
Growth Windows       : 3-Year, 5-Year and 10-Year
Edge Cases Supported : 6 Required Cases
Unit Tests           : 13/13 PASSED
Failed Tests         : 0
Day 10 Status        : COMPLETED SUCCESSFULLY