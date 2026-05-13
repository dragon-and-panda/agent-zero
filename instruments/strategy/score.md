# Strategy Scoring Instrument

`instruments/strategy/score.sh` evaluates a candidate revenue lane using four hard gates and five soft execution factors.

## Inputs

Pass factors as `key=value` pairs:

- hard gates: `legality`, `consent`, `provenance`, `tos`
- soft factors: `time`, `margin`, `repeatability`, `automation`, `defensibility`

Accepted values:

- `high`
- `medium`
- `low`

## Decision rules

- `REJECT`: any hard gate is not `high`
- `PASS`: all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`
- `HOLD`: all hard gates are `high`, but the lane is still weak on execution quality

## Example

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=high \
  time=high margin=medium repeatability=high automation=high defensibility=medium
```
