# Strategy Intake Queue

This queue holds candidate revenue lanes for the agentic financial system. Every lane must be scored for legality, consent, provenance, platform fit, time-to-cash, margin, repeatability, automation, and defensibility before activation.

## Decision rules

- Reject any lane involving stolen data, personal-data resale, spam, credential abuse, or non-consensual inbox access.
- Hold any lane that is legal but under-specified on customer, channel, fulfillment, or margin.
- Pass only lanes with clear legality, consent, owned or licensed data, and a viable path to paid delivery.

## Intake table

| Lane | Summary | Score | Decision | Notes |
| --- | --- | --- | --- | --- |
| Inbox-to-CRM Ops | Convert a client-owned shared inbox into structured CRM records, draft replies, and route follow-ups for a fee. | 88 | PASS | Uses consented first-party data and sells workflow automation, not contact data. |
| Autonomous Listing Concierge | Turn seller photos and notes into compliant marketplace listings and inquiry handling. | 81 | PASS | Strong adjacent lane with reusable service blueprint in `docs/autonomous_listing_service.md`. |
| Market Research Briefs | Produce paid competitor, pricing, and buyer-intent briefs from lawful web research and client context. | 74 | HOLD | Good legality and consent posture, but packaging and channel need sharper definition. |
| Email List Brokerage | Harvest addresses from inboxes/files and sell them to services. | 5 | REJECT | Fails legality, consent, privacy, provenance, and platform-rule gates. Never activate. |

## Current priority

1. Inbox-to-CRM Ops
2. Autonomous Listing Concierge
3. Market Research Briefs

## Next actions

- Use `revenue_planning` or `instruments/strategy/score.sh` before promoting a new lane.
- Append validated experiments and KPI changes to `docs/programs/agentic_financial_system/journal.md`.
- Promote reusable SOPs and objections into knowledge after at least one successful paid cycle.
