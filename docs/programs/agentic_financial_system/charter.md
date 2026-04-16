# Agentic Financial System Charter

## Mission

Build a self-sustaining revenue system around Agent Zero using lawful, ethical, and automatable online services. The system should compound through reusable tools, retained knowledge, and repeatable workflows rather than through privacy abuse, spam, or resale of personal data.

---

## What This Program Is

This program is a portfolio of revenue lanes that can be operated or assisted by autonomous agents with minimal human supervision.

The goal is not "make money by any means." The goal is:

- durable revenue,
- clean data practices,
- repeatable delivery,
- low coordination overhead,
- defensible operations that can scale.

---

## Non-Negotiable Guardrails

This program follows `docs/policies/compliance_pack.md`.

Explicitly out of scope:

- personal email list brokerage,
- inbox scraping for resale,
- non-consensual lead harvesting,
- spam automation,
- deceptive or policy-evasive outreach.

Any lane that depends on those patterns is rejected even if it appears fast.

---

## Approved Revenue Lanes

### Lane 1: Inbox-to-CRM Assistant

**Purpose**
- Convert owner-authorized inbox activity into structured, useful workflow outputs.

**Examples**
- classify inbound messages,
- extract companies, contacts, and requests from approved conversations,
- draft replies,
- sync customer-approved records into a CRM,
- create follow-up tasks and summaries.

**Constraints**
- owner authorization only,
- least-privilege OAuth,
- no resale of contacts,
- no unsolicited bulk outreach generated from inbox exports.

### Lane 2: Autonomous Listing and Catalog Services

**Purpose**
- Use AI workflows to improve item listings, catalog quality, and inquiry handling.

**Anchor**
- `docs/autonomous_listing_service.md`

**Why it fits**
- service revenue,
- clear customer value,
- strong automation potential,
- lawful with customer-owned inputs.

### Lane 3: Research and Productized Intelligence

**Purpose**
- Sell high-signal research outputs such as market scans, competitor briefs, pricing analyses, or operating reports.

**Why it fits**
- uses Agent Zero strengths in search, synthesis, and memory,
- minimal sensitive-data exposure,
- strong repeatability when templated.

### Lane 4: Client-Owned Workflow Automation

**Purpose**
- Build and run automations for businesses using data, inboxes, docs, and processes they already own and control.

**Examples**
- proposal generation,
- customer support triage,
- knowledge-base ingestion,
- internal operations dashboards,
- compliance-ready summaries and audit trails.

---

## Operating Model

1. Capture candidate lanes in `docs/strategy/incoming.md`.
2. Score each lane with `instruments/strategy/score.sh`.
3. Activate only lanes that clear hard gates and have acceptable operational attractiveness.
4. Record decisions and experiments in `journal.md`.
5. Maintain an improvement backlog in `improvements.md`.
6. Reuse successful assets across lanes through prompts, instruments, knowledge, and memory.

---

## Evaluation Criteria

Every lane is evaluated on:

- legality,
- consent,
- provenance,
- terms-of-service compatibility,
- time-to-value,
- margin potential,
- repeatability,
- automation fit,
- defensibility.

The intent is to favor businesses that get better as the system learns, not businesses that survive only through brittle arbitrage.

---

## Phase Structure

### Phase 0: Foundations
- establish compliance pack,
- create scoring and intake process,
- define approved lanes,
- seed journals and backlogs.

### Phase 1: First Revenue Proofs
- prioritize the inbox-to-CRM lane and listing-service lane,
- keep scope narrow,
- favor fast deployment with explicit customer value,
- gather reusable templates, prompts, and SOPs.

### Phase 2: Productization
- standardize onboarding,
- improve telemetry and reporting,
- reduce manual exception handling,
- package repeatable offers into fixed-scope products.

### Phase 3: Portfolio Management
- compare lane economics,
- reinvest in the best performers,
- retire low-margin or high-friction lanes,
- expand only where compliance and execution quality stay intact.

---

## Initial Priorities

1. **Inbox-to-CRM assistant**
   - Most direct replacement for the rejected email-list mission.
   - Turns inbox access into customer value without violating privacy.

2. **Autonomous listing service**
   - Strong adjacent service with an existing technical blueprint.

3. **Research reports**
   - Useful hedge with lower operational complexity.

---

## Success Signals

Track each lane against:

- number of active customers or internal deployments,
- revenue per engagement,
- gross margin profile,
- hours of manual intervention avoided,
- cycle time from intake to deliverable,
- retention or repeat-use rate,
- compliance incidents prevented,
- number of reusable assets created.

---

## Decision Rule

If a lane looks profitable only because it ignores consent, provenance, or platform rules, the correct move is not to optimize it. The correct move is to replace it with a compliant equivalent that can survive scrutiny and compound over time.
