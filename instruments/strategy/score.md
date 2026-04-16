# Strategy Opportunity Score Instrument

`instruments/strategy/score.sh` scores a candidate revenue lane for the agentic financial system.

## Inputs

Provide nine positional arguments using `low`, `medium`, or `high`:

1. legality
2. consent
3. provenance
4. tos
5. time
6. margin
7. repeatability
8. automation
9. defensibility

Example:

```bash
bash instruments/strategy/score.sh high high high high medium high high high medium
```

## Decision Logic

### REJECT
Returned when any hard gate fails:
- legality = low
- consent = low
- provenance = low
- tos = low

### HOLD
Returned when hard gates pass but the lane is not yet attractive enough to activate.

This includes:
- any soft factor set to `low`
- or a total weighted score below the pass threshold

### PASS
Returned only when:
- all hard gates are at least `medium`;
- all soft execution factors (`time`, `margin`, `repeatability`, `automation`, `defensibility`) are at least `medium`;
- and the weighted total reaches the pass threshold.

## Suggested Interpretation

- `PASS`: candidate is compliant and commercially strong enough to advance.
- `HOLD`: candidate may be lawful, but it needs refinement, better economics, or more automation leverage.
- `REJECT`: candidate should not enter the backlog in its current form.

## Sample Cases

### Compliant PASS
```bash
bash instruments/strategy/score.sh high high high high medium high high high medium
```

### Compliant but weak HOLD
```bash
bash instruments/strategy/score.sh high high high high low high medium medium medium
```

### Unsafe REJECT
```bash
bash instruments/strategy/score.sh high low low low high high high high high
```
