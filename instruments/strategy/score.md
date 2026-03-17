# Strategy Opportunity Scoring Instrument

This instrument helps rank candidate revenue opportunities before launching them.

## Purpose

Prefer offers that are:
- lawful,
- quick to validate,
- easy to automate,
- resilient to platform changes,
- affordable to start,
- supported by existing repo capabilities.

## Dimensions

Each opportunity is scored from 1-5 on:

- `legality`
- `speed_to_cash`
- `automation_fit`
- `demand_confidence`
- `resilience`
- `low_capital_intensity`

Weighted score:

```text
(legality * 3) +
(speed_to_cash * 2) +
(automation_fit * 2) +
(demand_confidence * 2) +
(resilience * 2) +
(low_capital_intensity * 1)
```

## Usage

Create a TSV file like:

```text
name	legality	speed_to_cash	automation_fit	demand_confidence	resilience	low_capital_intensity
Listing optimization service	5	4	4	4	4	5
Opt-in research newsletter	5	3	5	3	4	5
Paper-trading signal sandbox	4	1	4	2	3	4
```

Run:

```bash
bash instruments/strategy/score.sh opportunities.tsv
```

The script prints opportunities sorted by weighted score so the orchestrator can select a primary lane and a backup lane.
