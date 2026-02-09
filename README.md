# Autonomous Insurance Claims Processing Agent

A practical, testable prototype for first-pass insurance claim triage.

## Features

- Structured claim input model with validation.
- Deterministic risk scoring (low / medium / high).
- Decision output (approve / manual_review / reject).
- Recommended payout calculation with policy-limit capping.
- CLI interface for local simulation.
- Pytest unit tests for core scenarios.

## Run the agent

```bash
python3 agent.py --police-report
```

You can override inputs, for example:

```bash
python3 agent.py \
  --claim-id CLM-2026-0099 \
  --amount 9000 \
  --policy-limit 10000 \
  --incident-type collision \
  --claimant-tenure-years 0.4
```

## Run tests

```bash
python3 -m pytest -q
```

## Notes

This repository intentionally keeps the decision logic transparent and rule-based so it can be audited, tuned, and later replaced by more advanced models or orchestration.
