# Strategy Scoring Instrument

`score.sh` is a lightweight gate for monetization lanes. It is intentionally strict:

- hard gates: legality, consent, provenance, platform_fit
- soft factors: margin, repeatability, automation, defensibility, time_to_cash

## Usage

```bash
bash instruments/strategy/score.sh \
  legality consent provenance platform_fit \
  margin repeatability automation defensibility time_to_cash
```

Each value must be one of:

- `low`
- `medium`
- `high`

## Outcomes

- `REJECT`
  - any hard gate is `low`
- `HOLD`
  - any hard gate is `medium`
  - any soft factor is `low`
  - fewer than three soft factors are `high`
- `PASS`
  - all hard gates are `high`
  - no soft factor is `low`
  - at least three soft factors are `high`

## Examples

### REJECT

```bash
bash instruments/strategy/score.sh low high high high high high high high high
```

### HOLD

```bash
bash instruments/strategy/score.sh high high high high high medium high medium high
```

### PASS

```bash
bash instruments/strategy/score.sh high high high high high high high medium high
```
