# Agentic Financial System Improvement Queue

## Active lanes

### Lane 1: Inbox to CRM assistant
- Build a toolchain that summarizes user-owned Gmail or IMAP messages after explicit consent.
- Extract only business signals that support first-party workflows: lead status, follow-up deadlines, account risk, FAQ topics, and support backlog items.
- Store provenance and confidence with each extracted fact.
- Never export or resell raw personal contact data.

### Lane 2: Autonomous listing service
- Reuse `docs/autonomous_listing_service.md` as a compliant revenue lane.
- Prioritize seller-owned inventory, opt-in client onboarding, and performance-based pricing.
- Treat this lane as a hedge if inbox-to-CRM monetization stalls.

### Lane 3: Research products
- Package aggregated, anonymized market research, deliverability benchmarks, workflow templates, and sales playbooks.
- Sell insight and execution support, not scraped identities.

## Engineering backlog
- Add a first-class `revenue_planning` tool so the agent screens revenue ideas before taking action.
- Add prompt guardrails that reject personal-data resale, inbox scraping without consent, and other non-consensual workflows.
- Add an intake queue for scoring candidate ventures before activation.
- Add a strategy instrument that yields `PASS`, `HOLD`, or `REJECT` with clear reasons.
- Expand docs index links so the compliance pack and program docs are easy to discover.

## Deferred/high-risk items
- Any live trading or wagering lane beyond simulation.
- Any marketplace or workflow that would violate anti-spam, privacy, consumer protection, platform, or export rules.
- Any automation that touches regulated data without explicit retention, deletion, and audit policies.
