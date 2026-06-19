# Strategy Scoring Instrument

This instrument classifies an opportunity as PASS, HOLD, or REJECT using four risk inputs:

- legality risk: `low`, `medium`, `high`
- consent risk: `low`, `medium`, `high`
- provenance risk: `low`, `medium`, `high`
- platform risk: `low`, `medium`, `high`

## Rules

- Any `high` legality or provenance risk returns `REJECT`.
- Any `high` consent or platform risk returns `REJECT`.
- Any remaining `medium` risk returns `HOLD`.
- Only all-`low` inputs return `PASS`.

## Usage

```bash
./instruments/strategy/score.sh low low low low
./instruments/strategy/score.sh low medium low low
./instruments/strategy/score.sh high low low low
```

## Interpretation

- `PASS`: safe enough to move into planning and execution.
- `HOLD`: missing approvals, consent clarity, or platform confidence.
- `REJECT`: violates hard gates and should be redirected to a safer business model.
