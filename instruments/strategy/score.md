# Strategy Scoring Instrument

`instruments/strategy/score.sh` turns a candidate revenue lane into one of three outcomes:

- `PASS` - compliant and attractive enough to activate
- `HOLD` - compliant or potentially compliant, but still missing clarity or business quality
- `REJECT` - fails a hard gate and must not be activated

## Hard Gates

Rate each as `low`, `medium`, or `high`:

- `legality`
- `consent`
- `provenance`
- `platform_risk`

Interpretation:

- `low legality`, `low consent`, or `low provenance` -> `REJECT`
- `high platform_risk` -> `REJECT`
- any `medium` on hard gates -> `HOLD`

## Soft Factors

Rate each as `low`, `medium`, or `high`:

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

Interpretation:

- any soft factor at `low` keeps the lane on `HOLD`
- at least three soft factors must be `high` to get `PASS`

## Usage

```bash
./instruments/strategy/score.sh \
  legality=high \
  consent=high \
  provenance=high \
  platform_risk=low \
  time=medium \
  margin=high \
  repeatability=high \
  automation=high \
  defensibility=medium
```

## Example Outcomes

### PASS

```bash
./instruments/strategy/score.sh \
  legality=high consent=high provenance=high platform_risk=low \
  time=medium margin=high repeatability=high automation=high defensibility=medium
```

### HOLD

```bash
./instruments/strategy/score.sh \
  legality=high consent=medium provenance=high platform_risk=low \
  time=high margin=high repeatability=high automation=high defensibility=high
```

### REJECT

```bash
./instruments/strategy/score.sh \
  legality=low consent=low provenance=low platform_risk=high \
  time=high margin=high repeatability=high automation=high defensibility=high
```
