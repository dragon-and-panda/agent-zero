# Strategy Opportunity Scoring

Use `instruments/strategy/score.sh` to classify a lane as `PASS`, `HOLD`, or `REJECT`.

## Inputs

The script accepts ten positional arguments in this order:

1. legality
2. consent
3. provenance
4. platform_risk
5. time_to_cash
6. margin
7. repeatability
8. automation_fit
9. defensibility
10. notes

Each scored field must be one of:

- `low`
- `medium`
- `high`

The `notes` field is freeform text.

## Hard gates

The script returns `REJECT` immediately when any of these are true:

- legality is `low`
- consent is `low`
- provenance is `low`
- platform_risk is `high`

This keeps the system from progressing opportunities that depend on privacy abuse,
unclear data ownership, or likely terms-of-service violations.

## PASS criteria

The script returns `PASS` only when all hard gates clear and:

- legality, consent, provenance are `high`
- platform_risk is not `high`
- none of `time_to_cash`, `margin`, `repeatability`, `automation_fit`, or
  `defensibility` are `low`
- at least three of those five execution factors are `high`

## HOLD criteria

The script returns `HOLD` for compliant opportunities that still need work, such as:

- legitimate offers with slow time-to-cash
- ethical lanes with weak margin or limited repeatability
- promising ideas that need better automation or differentiation

## Examples

```bash
./instruments/strategy/score.sh high high high low high high high high medium "Opt-in local listing service"
./instruments/strategy/score.sh high high high medium medium high medium high low "Needs better moat"
./instruments/strategy/score.sh low low low high high high high high high "Personal email resale"
```
