# Strategy Scoring Instrument

`score.sh` turns a venture idea into a simple decision: `GO`, `HOLD`, or `REJECT`.

## Inputs
- `--name`: short venture name
- `--summary`: what the offer is, how it makes money, and key constraints
- `--time-to-cash`: 1-5, where 5 means the offer can validate quickly
- `--repeatability`: 1-5, where 5 means the work can be templatized
- `--compliance`: 1-5, where 5 means low legal/privacy/platform risk
- `--resilience`: 1-5, where 5 means the lane is resistant to platform or client shocks
- `--capital`: 1-5, where 5 means low capital intensity

## Hard fails
- Any idea centered on selling personal emails, scraped contacts, inbox exports, or similar personal data.
- Live leveraged trading, managed-account schemes, or guaranteed-return offers.

## Output logic
- Weighted score out of 100 using the six dimensions above.
- `GO`: score >= 75 and no policy triggers.
- `HOLD`: score 55-74, or simulation-only trading research.
- `REJECT`: score < 55 or any hard-fail policy trigger.

## Example
```bash
instruments/strategy/score.sh \
  --name "Inbox-to-CRM Hygiene Service" \
  --summary "Organize the owner's own inbox contacts into a CRM-ready sheet with consent-safe exports." \
  --time-to-cash 4 \
  --repeatability 4 \
  --compliance 5 \
  --resilience 4 \
  --capital 5
```
