# Strategy Score Instrument

This instrument screens revenue ideas before execution.

## Inputs

Each factor must be passed as one of:

- `low`
- `medium`
- `high`

Hard gates:

- legality
- consent
- provenance
- platform

Soft execution factors:

- time
- margin
- repeatability
- automation
- defensibility

## Decision rules

- REJECT: any hard gate is `low`
- HOLD: hard gates avoid `low`, but at least one hard gate is `medium`, or any soft factor is `low`, or fewer than three soft factors are `high`
- PASS: all hard gates are `high`, no soft factor is `low`, and at least three soft factors are `high`

## Usage

```bash
./instruments/strategy/score.sh \
  --legality high \
  --consent high \
  --provenance high \
  --platform high \
  --time medium \
  --margin high \
  --repeatability high \
  --automation high \
  --defensibility medium
```
