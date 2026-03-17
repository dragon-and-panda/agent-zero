# Opportunity Scoring Instrument

This instrument gives each venture a quick, comparable score before execution begins.

## Inputs

Each category uses a 0-10 score:
- `demand`: is there a real and reachable buyer problem?
- `speed`: how quickly can value be delivered and revenue tested?
- `fit`: how well does the current repo/agent stack support delivery?
- `compliance`: how safe is the model from legal, privacy, and platform risk?
- `repeatability`: can the work become a repeatable system or product?
- `resilience`: does the model have fallbacks and low dependency risk?

## Output bands

- `GO`: 44+ total and `compliance >= 7`
- `HOLD`: 32-43 total, or good score with material uncertainty
- `REJECT`: below 32, or `compliance < 7`

## Example

```bash
./instruments/strategy/score.sh \
  --name "Inbox-to-CRM Hygiene Service" \
  --demand 8 \
  --speed 8 \
  --fit 8 \
  --compliance 9 \
  --repeatability 7 \
  --resilience 8
```
