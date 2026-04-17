# Strategy Scoring Instrument

This instrument gives a fast PASS, HOLD, or REJECT decision for candidate revenue lanes.

## Usage

```bash
./instruments/strategy/score.sh legality consent provenance tos time margin repeatability automation defensibility
```

Each argument must be one of:

- `low`
- `medium`
- `high`

## Factors

Hard gates:

1. legality
2. consent
3. provenance
4. tos

Soft factors:

5. time
6. margin
7. repeatability
8. automation
9. defensibility

## Decision rules

- REJECT if any hard gate is `low`
- HOLD if hard gates are not weak enough to reject but any hard gate is below `high`
- HOLD if all hard gates are `high` but any soft factor is `low`
- PASS only when every hard gate is `high` and every soft factor is at least `medium`

## Example calls

```bash
./instruments/strategy/score.sh high high high high high high high medium medium
./instruments/strategy/score.sh high high high high low high high medium medium
./instruments/strategy/score.sh high low high high high high high high high
```
