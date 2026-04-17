# Strategy Scoring Instrument

This instrument scores candidate revenue lanes for the agentic financial system.

## Purpose

It is designed to prevent the system from chasing attractive-but-noncompliant ideas and to rank lawful opportunities by execution quality.

## Hard Gates

The script immediately returns `REJECT` if any of the following are not `high`:

- legality
- consent
- provenance
- tos

These are non-negotiable. If a lane fails even one hard gate, it should not proceed.

## Soft Execution Factors

After passing the hard gates, the script evaluates:

- time
- margin
- repeatability
- automation
- defensibility

### Outcomes

- `PASS`: all soft factors are `medium` or `high`, and none are `low`
- `HOLD`: hard gates passed, but at least one soft factor is `low`
- `REJECT`: one or more hard gates failed

## Usage

```bash
bash instruments/strategy/score.sh \
  legality=high \
  consent=high \
  provenance=high \
  tos=high \
  time=medium \
  margin=high \
  repeatability=high \
  automation=medium \
  defensibility=medium
```

## Interpretation

- Use `PASS` for lanes ready for scoping or MVP design.
- Use `HOLD` for compliant lanes that are still unattractive or too weak operationally.
- Use `REJECT` for lanes that should not proceed.
