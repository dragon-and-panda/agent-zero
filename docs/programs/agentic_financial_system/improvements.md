# Agentic Financial System Improvement Backlog

## Priority queue

1. Build a reusable authorized inbox-to-CRM playbook
   - define allowed mailbox scopes,
   - add provenance capture,
   - map extracted entities to CRM-ready fields.

2. Add a mission scoring ritual
   - evaluate every lane with `instruments/strategy/score.sh`,
   - log PASS, HOLD, or REJECT outcomes in the journal.

3. Productize the autonomous listing service
   - narrow the MVP,
   - document pricing hypotheses,
   - identify the first seller profile to target.

4. Stand up first-party audience capture
   - define lead magnet concepts,
   - capture explicit consent,
   - design segmentation workflows for permissioned contacts only.

5. Create a telemetry layer
   - margin, cycle time, acceptance rate, and automation coverage,
   - policy incident count and remediation logs.

## Guardrail improvements

- Require explicit authorization language before any inbox-processing workflow is marked ready.
- Prefer anonymized or consented datasets for Orange-based analytics.
- Add template prompts for unsubscribe, deletion, and provenance notices where applicable.
