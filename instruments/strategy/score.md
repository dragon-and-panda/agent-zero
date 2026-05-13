# Strategy Scoring Instrument

`score.sh` screens monetization ideas before they enter execution.

## Inputs

Hard gates:
- `legality=low|medium|high`
- `consent=low|medium|high`
- `provenance=low|medium|high`
- `platform_risk=low|medium|high`

Soft execution factors:
- `time=low|medium|high`
- `margin=low|medium|high`
- `repeatability=low|medium|high`
- `automation=low|medium|high`
- `defensibility=low|medium|high`

## Decision rules

- `REJECT` if any hard gate is `low`
- `PASS` only when all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`
- `HOLD` for everything else

## Example commands

### Reject
```bash
./instruments/strategy/score.sh legality=low consent=low provenance=low platform_risk=low
```

### Hold
```bash
./instruments/strategy/score.sh legality=high consent=high provenance=high platform_risk=high time=medium margin=high repeatability=medium automation=high defensibility=medium
```

### Pass
```bash
./instruments/strategy/score.sh legality=high consent=high provenance=high platform_risk=high time=high margin=high repeatability=high automation=high defensibility=medium
```
