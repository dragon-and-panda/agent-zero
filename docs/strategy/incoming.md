# Strategy Intake Queue

Use this queue for new revenue ideas before implementation.

## Decision rubric

- run `revenue_planning` first
- score approved candidates with `instruments/strategy/score.sh`
- reject ideas that fail legality, consent, provenance, or platform checks

## Queue

| Idea | Status | Notes |
| --- | --- | --- |
| Sell email lists compiled from Gmail and local files | rejected | Personal-data resale and non-consensual inbox extraction are prohibited. |
| Client-authorized inbox-to-CRM hygiene | active | Safe replacement for inbox processing; preserve consent and suppression state. |
| Autonomous listing optimization service | active | Leverages existing listing-service components in this repo. |
| Paid niche research briefs | active | Must use lawful public or licensed data only. |
| Affiliate content plus opt-in newsletter | active | Requires transparent disclosures and consent-based acquisition. |
