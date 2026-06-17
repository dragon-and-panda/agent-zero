# Agentic Financial System Backlog

This backlog tracks the next safest and highest-leverage improvements for the
agentic financial system. Every item must satisfy the compliance pack before it
can move into execution.

## Priority 1: First-party revenue lanes

1. Inbox-to-CRM ingestion for user-owned mailboxes with explicit consent.
   - Parse approved inbound messages into a structured CRM record.
   - Tag opportunities by intent, urgency, and likely service fit.
   - Draft compliant follow-up messages for human approval or policy-bounded send.
2. Autonomous listing optimization using the existing listing service blueprint.
   - Start with higher-margin local categories and client-owned inventory.
   - Add comp-based price ladders and reporting.
3. Research product lane.
   - Produce niche market maps, vendor lists, and intelligence briefs.
   - Sell reports or subscriptions rather than personal data.

## Priority 2: Controls and instrumentation

1. Add a budget guard extension for token and compute ceilings.
2. Add a watchdog extension that halts workflows on compliance keyword hits.
3. Add structured telemetry outputs for revenue, margin, and payback period.
4. Persist approved playbooks into memory for reuse.

## Priority 3: Better opportunity selection

1. Require all new ideas to run through `instruments/strategy/score.sh`.
2. Add comparable-offer templates for service pricing.
3. Build a rejection log of unsafe or low-quality revenue ideas to prevent repeats.

## Rejected classes of work

- Buying, scraping, brokering, or selling contact lists.
- Non-consensual mailbox mining.
- Sending outreach that violates anti-spam laws or platform rules.
- Workflows that conceal identity, provenance, or commercial intent.
