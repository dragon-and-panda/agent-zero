# Strategy scoring instrument

Purpose:
- Screen proposed revenue lanes before activation.
- Reject anything that fails legality, consent, provenance, or platform-rule checks.
- Distinguish between compliant opportunities that are attractive now (`PASS`) and compliant ones that still need work (`HOLD`).

Inputs:
- `legality`: `low|medium|high`
- `consent`: `low|medium|high`
- `provenance`: `low|medium|high`
- `tos`: `low|medium|high`
- `time`: `low|medium|high`
- `margin`: `low|medium|high`
- `repeatability`: `low|medium|high`
- `automation`: `low|medium|high`
- `defensibility`: `low|medium|high`

Interpretation:
- Hard gates: legality, consent, provenance, tos
- Soft factors: time, margin, repeatability, automation, defensibility

Decision rules:
1. If any hard gate is `low`, return `REJECT`.
2. If any hard gate is `medium`, return `HOLD`.
3. If all hard gates are `high` but any soft factor is `low`, return `HOLD`.
4. If all hard gates are `high` and all soft factors are `medium|high`, return `PASS`.

Examples:
- Inbox-to-CRM assistant for the operator's own business with opt-in leads:
  `high high high high medium high high medium medium` -> `PASS`
- Marketplace arbitrage idea with unclear platform terms:
  `high high high medium medium medium medium medium low` -> `HOLD`
- Buying/selling scraped email lists:
  `low low low low high high high high medium` -> `REJECT`
