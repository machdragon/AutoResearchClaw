# Experiment Specification

## Topic
Parameter Golf val_bpb minimization — lane_3: QAT + roundtrip-aware compression alignment. Hypothesis: If we enable staged QAT aligned to int8+zlib roundtrip, post-roundtrip val_bpb will improve versus float-only training under the same gate budget. Artifact limit 16MB. Quick-gate: runtime <= 1.10x baseline.

## Project Structure
Multi-file experiment project with 1 file(s): `main.py`

## Entry Point
`main.py` — executed directly via sandbox

## Outputs
- `main.py` emits metric lines in `name: value` format
- Primary metric key: `val_bpb`

## Topic-Experiment Alignment
ALIGNED

## Constraints
- Time budget per run: 1200s
- Max iterations: 2
- Self-contained execution (no external data, no network)
- Validated: Code validation passed.

## Generated
2026-03-19T23:24:49+00:00
