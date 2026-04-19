# Strategy Scoring Instrument

Score every proposed revenue lane with the shell script in this directory before activation.

## Inputs

Each factor accepts one of:

- `low`
- `medium`
- `high`

Required factors:

- legality
- consent
- provenance
- platform
- time
- margin
- repeatability
- automation
- defensibility

## Hard gates

Immediately reject the lane if any of these are `low`:

- legality
- consent
- provenance
- platform

These represent non-negotiable controls.

## Soft scoring

The lane returns:

- `PASS` when every soft factor is at least `medium` and at least three soft factors are `high`
- `HOLD` when hard gates pass but the opportunity is not yet strong enough to activate
- `REJECT` when any hard gate fails

## Example commands

```bash
./instruments/strategy/score.sh legality=high consent=high provenance=high platform=high time=high margin=high repeatability=high automation=medium defensibility=medium

./instruments/strategy/score.sh legality=high consent=high provenance=high platform=high time=medium margin=medium repeatability=medium automation=medium defensibility=low

./instruments/strategy/score.sh legality=high consent=low provenance=high platform=high time=high margin=high repeatability=high automation=high defensibility=high
```
