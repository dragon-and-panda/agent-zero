# Strategy Scoring Instrument

Score each candidate lane before activation.

## Inputs

Provide each factor as `low`, `medium`, or `high`.

### Hard gates

- `legality`
- `consent`
- `provenance`
- `platform_fit`

### Soft factors

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

## Decision rules

- `REJECT` if any hard gate is `low`
- `HOLD` if any hard gate is `medium`
- `HOLD` if any soft factor is `low`
- `PASS` only when all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`

## Example runs

### Reject

```bash
./instruments/strategy/score.sh \
  legality=low consent=low provenance=low platform_fit=low \
  time=high margin=high repeatability=high automation=high defensibility=medium
```

### Hold

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_fit=high \
  time=medium margin=high repeatability=medium automation=high defensibility=medium
```

### Pass

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_fit=high \
  time=high margin=high repeatability=high automation=medium defensibility=high
```
