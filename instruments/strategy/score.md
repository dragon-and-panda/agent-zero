# Strategy Score Instrument

This instrument scores a proposed revenue lane using four hard factors and five soft factors.

## Usage

```bash
instruments/strategy/score.sh \
  <legality> \
  <consent> \
  <provenance> \
  <platform_risk> \
  <time_to_cash> \
  <margin> \
  <repeatability> \
  <automation> \
  <defensibility>
```

Each argument must be one of:

- `low`
- `medium`
- `high`

## Factor meanings

Hard factors:

- `legality`: confidence that the lane is lawful
- `consent`: confidence that the relevant parties agreed to the use
- `provenance`: confidence that the data source is authorized and well understood
- `platform_risk`: risk of violating platform rules or terms; `low` is good, `high` is bad

Soft factors:

- `time_to_cash`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

## Verdict rules

- `REJECT` if legality, consent, or provenance is `low`, or if platform risk is `high`
- `HOLD` if any hard factor is conservative (`medium` or worse for the positive factors, `medium` or worse for platform risk), if any soft factor is `low`, or if fewer than three soft factors are `high`
- `PASS` only if all hard factors are fully clear, no soft factor is `low`, and at least three soft factors are `high`

## Examples

### PASS

```bash
instruments/strategy/score.sh high high high low medium high high high medium
```

### HOLD

```bash
instruments/strategy/score.sh high high high low medium medium high medium medium
```

### REJECT

```bash
instruments/strategy/score.sh medium low medium high high high high high high
```
