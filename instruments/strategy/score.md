# Problem
Evaluate a proposed revenue lane before building or activating it.

# Solution
Run:

```bash
bash /a0/instruments/strategy/score.sh \
  --lane "Inbox-to-CRM" \
  --legality high \
  --consent high \
  --provenance high \
  --tos high \
  --time medium \
  --margin medium \
  --repeatability high \
  --automation high \
  --defensibility medium
```

## Inputs

Use only `low`, `medium`, or `high` for each factor:

- `legality`
- `consent`
- `provenance`
- `tos`
- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

## Output

The instrument returns:

- `REJECT` when legality, consent, provenance, or TOS is weak;
- `PASS` when the lane clears hard gates and the weighted score is strong;
- `HOLD` when the lane is compliant but not yet attractive enough to activate.

## Examples

### PASS
```bash
bash /a0/instruments/strategy/score.sh \
  --lane "Opt-in newsletter" \
  --legality high --consent high --provenance high --tos high \
  --time medium --margin medium --repeatability high --automation high --defensibility medium
```

### HOLD
```bash
bash /a0/instruments/strategy/score.sh \
  --lane "Custom research sprint" \
  --legality high --consent high --provenance high --tos high \
  --time low --margin high --repeatability medium --automation low --defensibility high
```

### REJECT
```bash
bash /a0/instruments/strategy/score.sh \
  --lane "Sell harvested email lists" \
  --legality low --consent low --provenance low --tos low \
  --time high --margin high --repeatability high --automation high --defensibility low
```
