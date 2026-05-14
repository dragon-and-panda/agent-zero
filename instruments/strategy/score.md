# Strategy Scoring Instrument

This instrument screens a revenue lane before the agent spends time building it.

## Ratings

Every factor must be rated as one of:

- `low`
- `medium`
- `high`

## Hard gates

These control whether a lane is even eligible to run:

- `legality`
- `consent`
- `provenance`
- `platform_fit`

Rules:

- any hard gate rated `low` => `REJECT`
- all hard gates must be `high` for `PASS`
- any hard gate rated `medium` => `HOLD`

## Soft factors

These shape whether a compliant lane is worth automating now:

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

Rules:

- any soft factor rated `low` => `HOLD`
- `PASS` requires at least 3 soft factors rated `high`
- compliant lanes that are still weak or unclear stay in `HOLD`

## Usage

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_fit=high \
  time=high margin=medium repeatability=high automation=high defensibility=medium
```

## Example outcomes

- compliant and attractive => `PASS`
- compliant but unclear or weak => `HOLD`
- illegal, non-consensual, or poor-provenance => `REJECT`
