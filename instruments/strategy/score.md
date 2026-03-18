# Opportunity Scoring Instrument

`score.sh` provides a lightweight screening step for new revenue ideas. It is intentionally opinionated: ideas that rely on unconsented data, spam, or unsafe financial risk should fail fast.

---

## Usage

```bash
./instruments/strategy/score.sh \
  --name "Inbox-to-CRM Hygiene Service" \
  --legality 5 \
  --consent 5 \
  --profit 4 \
  --automation 4 \
  --speed 3 \
  --repeatability 4 \
  --capital 2 \
  --platform-risk 2 \
  --downside 2 \
  --notes "Client-authorized mailbox cleanup and CRM export"
```

---

## Rubric

Rate each field from 1 to 5:

- `legality`: clarity of legal basis
- `consent`: clarity of permission for any personal or contact data
- `profit`: gross margin and pricing power
- `automation`: how much of delivery can be systematized
- `speed`: time to first revenue
- `repeatability`: likelihood of repeat demand
- `capital`: capital intensity, where 1 is low and 5 is high
- `platform-risk`: dependence on fragile platforms, where 1 is low and 5 is high
- `downside`: severity of failure mode, where 1 is low and 5 is high

---

## Decision Rules

- Auto-REJECT if legality or consent are below 4.
- Auto-REJECT if notes indicate email list brokerage, spam, phishing, credential abuse, or unconsented inbox scraping.
- Auto-HOLD if notes indicate Forex, options, leverage, or similar trading activity.
- Otherwise:
  - `GO` for scores 75 and above
  - `HOLD` for scores 60-74
  - `REJECT` below 60

Record final decisions in `docs/strategy/incoming.md`.
