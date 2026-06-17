# Strategy Intake Queue

## Intake rules
- Every opportunity must pass legality, consent, data provenance, and platform-rule checks before execution.
- Any proposal involving non-consensual inbox access, scraping private contact data, spam, or resale of personal data is rejected immediately.
- Prefer first-party or opt-in assets: customer-owned CRM data, explicit subscriptions, public-business datasets, licensed data, and user-consented analytics.

## Current opportunities

### Rejected
1. Personal email list brokerage
   - Status: rejected
   - Reason: depends on personal-data extraction and resale without consent; high privacy, spam, and platform-abuse risk.
   - Replacement: build opt-in acquisition systems, inbox-to-CRM analytics for account owners, or first-party research products.

### Active candidates
1. Inbox-to-CRM enrichment for consenting operators
   - Inputs: user-authorized mailbox exports or APIs, customer-owned CRM, consent logs
   - Revenue mode: service fees, usage-based SaaS, setup retainers
   - Notes: summarize threads, classify leads, extract deal metadata, and draft compliant follow-ups for human review

2. Autonomous listing optimization service
   - Inputs: client-provided catalog/listing data, public market observations, image assets
   - Revenue mode: managed services, subscriptions, performance bonuses
   - Notes: adjacent to `docs/autonomous_listing_service.md`

3. Niche research and benchmarking products
   - Inputs: public sources, licensed datasets, first-party telemetry
   - Revenue mode: subscriptions, consulting packages, recurring reports
   - Notes: productize insights instead of reselling contact data

## Activation checklist
1. Score the lane with `instruments/strategy/score.sh`
2. Attach the relevant policy references from `docs/policies/compliance_pack.md`
3. Record launch decision and next experiment in `docs/programs/agentic_financial_system/journal.md`
