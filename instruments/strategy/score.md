# Strategy Scoring Instrument

Use `score.sh` to rank a lane after the hard-gate details are known.

## Inputs

Hard gates:
- legality
- consent
- provenance
- tos

Soft factors:
- time
- margin
- repeatability
- automation
- defensibility

Each input must be one of:
- low
- medium
- high

## Verdict rules

- REJECT:
  - any hard gate is `low`
- PASS:
  - every hard gate is `high`
  - no soft factor is `low`
  - at least three soft factors are `high`
- HOLD:
  - everything else

## Examples

PASS:

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=high \
  time=medium margin=high repeatability=high automation=high defensibility=medium
```

HOLD:

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=medium \
  time=high margin=medium repeatability=medium automation=high defensibility=medium
```

REJECT:

```bash
bash instruments/strategy/score.sh \
  legality=high consent=low provenance=high tos=high \
  time=high margin=high repeatability=high automation=high defensibility=medium
```
