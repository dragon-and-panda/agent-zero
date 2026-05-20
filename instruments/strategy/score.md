# Strategy Scoring Instrument

Use `score.sh` to screen monetization lanes before the agent spends time building or launching them.

## Inputs

Every factor uses one of: `low`, `medium`, `high`

### Hard gates
- `legality`
- `consent`
- `provenance`
- `platform_risk`

### Soft factors
- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

## Usage

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_risk=low \
  time=medium margin=high repeatability=high automation=high defensibility=medium
```

## Decision rules

- `REJECT` if legality, consent, or provenance are `low`, or if platform risk is `high`
- `HOLD` if any hard gate is `medium`
- `PASS` only when:
  - all hard gates clear,
  - no soft factor is `low`,
  - at least three soft factors are `high`
- otherwise `HOLD`

This preserves a meaningful middle state for compliant but unattractive opportunities.
