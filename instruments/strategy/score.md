# Strategy Scoring Instrument

This instrument screens revenue lanes using four hard gates and five execution factors.

## Usage

```bash
bash instruments/strategy/score.sh \
  legality consent provenance platform_risk \
  time_to_cash margin repeatability automation defensibility
```

Each input must be one of:

- `low`
- `medium`
- `high`

## Meanings

- `legality`: how clear and defensible the legal basis is
- `consent`: whether the data use and outreach path are consent-based or otherwise clearly authorized
- `provenance`: how trustworthy and authorized the data source is
- `platform_risk`: dependency on risky automation or likely terms-of-service conflicts; `low` is good and `high` is bad
- `time_to_cash`: `high` means faster path to first revenue
- `margin`: `high` means stronger unit economics
- `repeatability`: `high` means the lane can run repeatedly without bespoke work every time
- `automation`: `high` means a larger share of the workflow can be automated reliably
- `defensibility`: `high` means harder to commoditize and easier to retain advantage

## Decision rules

- REJECT if legality, consent, or provenance is `low`
- REJECT if platform_risk is `high`
- HOLD if any hard gate is `medium`
- HOLD if any execution factor is `low`
- PASS only when hard gates are clear, no execution factor is low, and at least three execution factors are high
