# Strategy Scoring Instrument

This instrument classifies a candidate revenue lane as PASS, HOLD, or REJECT.

## Inputs

Pass nine ratings in this order:

1. legality
2. consent
3. provenance
4. platform_alignment
5. time_to_cash
6. margin
7. repeatability
8. automation_fit
9. defensibility

Each rating must be one of:

- `low`
- `medium`
- `high`

## Output Rules

- `REJECT`: any hard gate is `low`.
- `PASS`: all hard gates are `high`, none of the soft factors are `low`, and at least three soft factors are `high`.
- `HOLD`: everything else.

Hard gates are legality, consent, provenance, and platform alignment.

## Example

```bash
bash instruments/strategy/score.sh high high high high medium medium high high medium
```
