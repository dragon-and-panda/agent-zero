# Strategy Score Instrument

This instrument screens candidate revenue lanes before execution.

## Inputs

Provide nine ratings in this order:

1. legality
2. consent
3. provenance
4. platform_alignment
5. time_to_cash
6. margin
7. repeatability
8. automation
9. defensibility

Each value must be one of:

- `low`
- `medium`
- `high`

## Decision rules

- Any hard gate rated `low` => `REJECT`
- Any hard gate rated `medium` => `HOLD`
- If all hard gates are `high` but any soft factor is `low` => `HOLD`
- `PASS` only when all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`
- Otherwise => `HOLD`

Hard gates:

- legality
- consent
- provenance
- platform_alignment

Soft factors:

- time_to_cash
- margin
- repeatability
- automation
- defensibility

## Example

```bash
bash instruments/strategy/score.sh \
  high high high high \
  medium medium high high medium
```
