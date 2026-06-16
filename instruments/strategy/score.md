# Strategy Scoring Instrument

`score.sh` evaluates a proposed revenue lane with four hard gates and five business-attractiveness factors.

## Inputs

Pass nine values in this order:

1. legality
2. consent
3. provenance
4. platform_compliance
5. time_to_cash
6. margin
7. repeatability
8. automation_leverage
9. defensibility

Each value must be one of:

- `low`
- `medium`
- `high`

## Rules

- If any hard gate is `low`, verdict is `REJECT`.
- If all hard gates are at least `medium`, but one or more are not `high`, verdict is `HOLD`.
- If all hard gates are `high`, then:
  - `PASS` requires every business factor to be at least `medium`
  - `PASS` also requires at least three business factors to be `high`
  - otherwise verdict is `HOLD`

## Example runs

### Reject

```bash
./instruments/strategy/score.sh low high high high high high high high high
```

### Hold

```bash
./instruments/strategy/score.sh high high high high low high high medium medium
```

### Pass

```bash
./instruments/strategy/score.sh high high high high medium high high high medium
```
