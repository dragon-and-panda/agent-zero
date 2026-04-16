# Agentic Financial System Improvement Backlog

This backlog tracks the highest-leverage improvements for the compliant revenue program.

## Current Priorities

### 1. Inbox-to-CRM Blueprint
- Define the minimum authorized mailbox ingestion workflow.
- Specify fields, consent handling, and CRM handoff format.
- Add a first-pass instrument for extracting structured opportunities from owner-authorized email.

### 2. Opportunity Intake Discipline
- Require each new idea to be logged in `docs/strategy/incoming.md`.
- Score each idea using `instruments/strategy/score.sh`.
- Reject lanes that fail legality, consent, provenance, or TOS checks before technical work begins.

### 3. Listing-Service Activation Path
- Connect the financial-system charter to `docs/autonomous_listing_service.md`.
- Identify the smallest deployable listing-service offer with clean inputs and clear KPIs.
- Define telemetry for listing throughput, response time, and conversion lift.

### 4. Research Product Packaging
- Select one niche research brief format the system can produce repeatedly.
- Standardize source citation and confidence notation.
- Create a delivery checklist for one-off reports vs. subscription intelligence.

### 5. Compliance Observability
- Add a lightweight mechanism that logs which guardrail caused a lane to be held or rejected.
- Consider a future extension hook that injects the compliance pack into high-risk workflows automatically.

## Candidate Future Instruments
- `instruments/strategy/score.sh` (current)
- `instruments/strategy/intake_checklist.sh`
- `instruments/crm/email_extract.py`
- `instruments/ops/telemetry_push.sh`
- `python/extensions/_35_budget_guard.py`
- `python/extensions/_40_watchdog.py`

## Next Experiment Queue
1. Score a compliant inbox-to-CRM lane using only first-party email.
2. Score a listing-service lane based on seller-provided inventory.
3. Score a research-brief lane based on public and licensed information.
4. Draft the smallest instrument for one passing lane and document the operating procedure.
