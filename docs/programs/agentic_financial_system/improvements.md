# Agentic Financial System Improvement Backlog

## Active priorities

1. Build a consent-aware inbox-to-CRM workflow definition and sample schemas.
2. Connect the existing autonomous listing service scaffold to the mission diary and scoring gate.
3. Add lightweight telemetry for opportunity scoring outcomes and lane status transitions.
4. Create a reusable prompt pack for service packaging, pricing, and offer design.
5. Add a watchdog extension that flags prohibited data-resale plans before execution.

## Candidate experiments

### Inbox-to-CRM lane

- evaluate lawful Gmail export ingestion patterns for first-party use
- define thread summarization and contact deduplication outputs
- create a pricing matrix for managed service versus software subscription

### Autonomous listing lane

- connect listing request intake to a profitability rubric
- add fee models for fixed-price, concierge, and revenue-share variants
- define platform-specific publishing adapters with compliance notes

### Research-product lane

- create a template for niche market maps and pricing intelligence reports
- define opt-in lead capture assets tied to report distribution
- package follow-on implementation retainers from research deliverables

## Exit criteria for production lanes

- legality, consent, provenance, and platform terms are all documented
- a lane scores PASS or justified HOLD through `instruments/strategy/score.sh`
- offer packaging and operating steps are documented well enough for autonomous reuse
- at least one measurable route to revenue is defined without personal-data resale
