# Problem
Score a proposed revenue opportunity before the agent invests time or data access into it.

# Inputs
Run:

```bash
bash /a0/instruments/strategy/score.sh <customer_value> <execution_feasibility> <repeatability> <legal_risk> <consent_risk> <data_provenance_risk> <platform_risk>
```

Each value must be `low`, `medium`, or `high`.

# Rules
1. If `legal_risk`, `consent_risk`, or `data_provenance_risk` is `high`, the result is `REJECT`.
2. If `platform_risk` is `high`, the result is at least `HOLD`.
3. Otherwise, combine upside and risk:
   - high upside with low-to-medium risk => `PASS`
   - everything else => `HOLD`

# Guidance
- Prefer first-party, consent-based, or licensed data.
- Reject any plan that depends on personal-data resale, unauthorized inbox access, or spam.
- Use this score before creating a new mission under `docs/strategy/incoming.md`.
