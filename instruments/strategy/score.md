# Opportunity Scoring Instrument

`score.sh` is a lightweight gate for deciding whether a candidate lane should move forward.

## Inputs

Run the script with nine values:

```bash
./instruments/strategy/score.sh \
  legality consent provenance tos \
  time margin repeatability automation defensibility
```

Each value must be one of:
- `low`
- `medium`
- `high`

## Factor Meaning

Hard gates:
- `legality`: confidence that the lane is lawful
- `consent`: confidence that data use is authorized
- `provenance`: clarity and traceability of data sources
- `tos`: confidence that the workflow respects platform rules

Soft execution factors:
- `time`: how quickly the lane can reach usable output
- `margin`: unit economics
- `repeatability`: ability to reuse the workflow across customers or cycles
- `automation`: degree of low-touch delivery
- `defensibility`: ability to maintain an advantage through process, data, trust, or integration

## Output Rules

- `REJECT` if any hard gate is not `high`
- `PASS` only if all hard gates are `high` and none of the soft factors are `low`
- `HOLD` if the lane is compliant but at least one soft factor is `low`

## Example Runs

```bash
# PASS
./instruments/strategy/score.sh high high high high high medium high high medium

# HOLD
./instruments/strategy/score.sh high high high high low high high medium medium

# REJECT
./instruments/strategy/score.sh high low high high high high high high high
```
