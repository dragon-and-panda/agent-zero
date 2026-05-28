# Strategy Score Instrument

Use `score.sh` to classify a proposed revenue lane as PASS, HOLD, or REJECT.

## Required hard-gate factors

- `legality`: `low|medium|high`
- `consent`: `low|medium|high`
- `provenance`: `low|medium|high`
- `platform_risk`: `low|medium|high`

Hard-gate rules:

- `legality` must be `high`,
- `consent` must be `high`,
- `provenance` cannot be `low`,
- `platform_risk` cannot be `high`.

If any hard-gate rule fails, the lane is `REJECT`.

## Soft execution factors

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

All soft factors use `low|medium|high`.

Soft scoring rules:

- any `low` soft factor forces `HOLD`,
- at least three `high` soft factors and no `low` soft factors allow `PASS`,
- otherwise the lane stays `HOLD`.

## Example calls

### PASS

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_risk=low \
  time=high margin=high repeatability=high automation=medium defensibility=medium
```

### HOLD

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=medium platform_risk=medium \
  time=medium margin=medium repeatability=high automation=medium defensibility=medium
```

### REJECT

```bash
./instruments/strategy/score.sh \
  legality=medium consent=low provenance=low platform_risk=high \
  time=high margin=high repeatability=high automation=high defensibility=high
```
