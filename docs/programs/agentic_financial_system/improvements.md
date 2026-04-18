# Agentic Financial System Improvement Backlog

This backlog captures the next iterations for the compliant financial-system program.

## Current Priorities

1. **Inbox-to-CRM assistant**
   - Build a customer-owned workflow that classifies inbound messages and drafts replies for opted-in contacts.
   - Require explicit account ownership and document retention/deletion rules.
2. **Revenue-planning automation**
   - Expand the planning tool to emit structured JSON suitable for dashboards and downstream orchestration.
   - Add memory hooks so approved lanes are easier to recall in later runs.
3. **Scoring telemetry**
   - Persist score outputs into mission logs so pass/hold/reject decisions are auditable over time.
4. **Compliant RAG ingestion**
   - Build a provenance-aware ingestion path for customer-supplied documents, public datasets, and licensed sources.
   - Reject personal inbox ingestion unless the lane is strictly first-party and properly authorized.
5. **Autonomous listing adjacency**
   - Reuse learnings from `docs/autonomous_listing_service.md` as a diversification hedge for near-term revenue.

## Later Bets

- First-party operations copilots for appointment scheduling, support triage, and quote generation.
- Public-data research reports sold as subscriptions or project deliverables.
- Prompt/instrument packs for repeatable managed services.

## Guardrail Reminder

Remove or reframe any item that drifts toward:

- contact-list resale,
- non-consensual outreach,
- mailbox scraping for third parties,
- or any other workflow blocked by `docs/policies/compliance_pack.md`.
