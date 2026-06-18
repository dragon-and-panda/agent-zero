# Strategy Score Instrument

Scores a venture lane with hard compliance gates plus soft commercial factors.

## Location

`instruments/strategy/score.sh`

## Inputs

Pass nine positional values using only `low`, `medium`, or `high`:

1. legality
2. consent
3. provenance
4. platform
5. time_to_cash
6. margin
7. repeatability
8. automation
9. defensibility

## Output logic

- `REJECT` if any hard gate is `low`
- `HOLD` if any hard gate is `medium`
- `HOLD` if all hard gates are `high` but any soft factor is `low`
- `PASS` only when:
  - all hard gates are `high`
  - no soft factor is `low`
  - at least three soft factors are `high`
- otherwise `HOLD`

## Examples

Reject a non-compliant lane:

```bash
bash instruments/strategy/score.sh low high high high high high high high high
```

Hold a compliant but weak lane:

```bash
bash instruments/strategy/score.sh high high high high medium medium high medium medium
```

Pass a strong compliant lane:

```bash
bash instruments/strategy/score.sh high high high high high high high medium high
```
