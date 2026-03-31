# Agentic Financial System Revenue Plan

## Objective
Build a durable, lawful revenue stack that can be operated by agents with limited human supervision while preserving consent, privacy, auditability, and service quality.

## Phase gates
Advance only when the current phase has repeatable inputs, measurable outputs, and written operating procedures.

### Phase 0: policy and scoring foundation
- Use `docs/policies/compliance_pack.md` as the baseline policy.
- Score every proposed lane with `instruments/strategy/score.sh`.
- Reject any lane that depends on scraping private inboxes, brokering personal contact lists, deceptive outreach, or regulatory shortcuts.

### Phase 1: fast, compliant service revenue
Priority is on services that monetize first-party or client-owned data.

#### Lane A: inbox-to-CRM hygiene service
- Input: consented access to a client inbox or exported mailbox.
- Agent tasks:
  - classify inbound messages,
  - extract structured contact and company data,
  - deduplicate records,
  - draft CRM updates and follow-up queues,
  - create a clean export for the client.
- Deliverables:
  - cleaned contact database,
  - segmented pipeline report,
  - reply drafts and task queue.
- Revenue model:
  - setup fee,
  - monthly retainer,
  - usage-based add-ons for cleanup volume.

#### Lane B: autonomous listing and resale concierge
- Use the existing listing-service blueprint to create, publish, and manage client-owned listings.
- Keep agent actions inside platform rules and human-approved pricing/negotiation limits.
- Revenue model:
  - per-listing fee,
  - success fee,
  - subscription for ongoing catalog management.

#### Lane C: research packs and market-monitoring briefs
- Produce curated opportunity maps, vendor landscapes, competitor watches, or niche market lists from public and licensed sources.
- Revenue model:
  - one-off research package,
  - recurring intelligence subscription.

### Phase 2: productized internal tooling
- Convert repeatable service workflows into lightweight operator tools or templates.
- Examples:
  - CRM cleanup playbooks,
  - lead qualification boards using opt-in data,
  - listing performance dashboards,
  - pricing recommendation copilots.
- Revenue model:
  - subscription software,
  - implementation fee,
  - training package.

### Phase 3: scaled multi-lane operation
- Run multiple compliant lanes in parallel.
- Track channel mix, contribution margin, refund rate, and failure rate.
- Promote only lanes with strong retention, low compliance drag, and low manual exception load.

## Operating rules
- Every lane must have:
  - a lawful data source,
  - a clear buyer,
  - a delivery workflow,
  - a refund/remediation path,
  - metrics for quality and margin.
- Every outbound communication workflow must:
  - rely on consent or legitimate first-party relationship,
  - disclose automation where required,
  - enforce rate limits and review thresholds.

## Immediate next bets
1. Score the inbox-to-CRM hygiene service.
2. Score the autonomous listing service.
3. Draft one repeatable research brief product.
4. Reject personal email list resale as a non-starter.
