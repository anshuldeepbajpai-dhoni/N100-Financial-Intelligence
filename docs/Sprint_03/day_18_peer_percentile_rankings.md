# Sprint 03 – Day 18 Report

## Module
Peer Percentile Rankings

## Objective
Enhance the Peer Comparison module by calculating percentile rankings for key financial metrics within each sector.

## Work Completed

- Developed `src/peer/percentile.py`.
- Calculated sector-wise percentile rankings for:
  - Return on Equity (ROE)
  - Return on Capital Employed (ROCE)
  - Operating Profit Margin (OPM)
  - Net Profit
  - Market Capitalization
- Integrated percentile calculation into `PeerEngine`.
- Updated `peer_runner.py` to execute the enhanced comparison process.
- Extended `export.py` to generate percentile output files.

## Files Created

- `src/peer/percentile.py`

## Files Modified

- `src/peer/engine.py`
- `src/peer/export.py`

## Output Files

- `output/peer/peer_comparison.csv`
- `output/peer/peer_rankings.csv`
- `output/peer/peer_percentiles.csv`
- `output/peer/peer_summary.csv`

## Validation

- Successfully executed the Peer Comparison pipeline.
- Verified percentile calculations.
- Confirmed CSV exports.

## Status

✅ Completed Successfully