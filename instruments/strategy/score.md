# Strategy Opportunity Scoring

Use `score.sh` to classify a monetization lane as `PASS`, `HOLD`, or `REJECT`.

## Hard gates

These gates must never be weak:

- `legality`
- `consent`
- `provenance`
- `tos`

Allowed values: `high`, `medium`, `low`

Any hard gate with `low` returns `REJECT`.

## Soft execution factors

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

Allowed values: `high`, `medium`, `low`

## Decision logic

- `REJECT`: any hard gate is `low`
- `PASS`: all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`
- `HOLD`: everything else

## Usage

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=high \
  time=medium margin=high repeatability=high automation=high defensibility=medium
```

The script prints the decision, a short rationale, and the normalized factor map.
