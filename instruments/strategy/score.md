# Strategy Scoring Instrument

Use `score.sh` to quickly gate venture ideas before execution.

## Inputs

- `impact`: low | medium | high
- `effort`: low | medium | high
- `durability`: low | medium | high
- `leverage`: low | medium | high
- `legality`: clear | unclear | blocked
- `consent`: verified | limited | missing
- `provenance`: first-party | licensed | unclear | scraped | purchased
- `platform_risk`: low | medium | high

## Decision rules

- REJECT when legality is not clear, consent is missing, or provenance is scraped or purchased
- HOLD when the idea may be legal but controls are incomplete or platform risk is high
- PASS when legality, consent, provenance, and platform risk are all acceptable

## Examples

### PASS

```bash
bash instruments/strategy/score.sh \
  impact=high effort=medium durability=high leverage=high \
  legality=clear consent=verified provenance=first-party platform_risk=low
```

### HOLD

```bash
bash instruments/strategy/score.sh \
  impact=medium effort=medium durability=medium leverage=medium \
  legality=clear consent=limited provenance=licensed platform_risk=high
```

### REJECT

```bash
bash instruments/strategy/score.sh \
  impact=medium effort=low durability=low leverage=low \
  legality=blocked consent=missing provenance=purchased platform_risk=high
```
