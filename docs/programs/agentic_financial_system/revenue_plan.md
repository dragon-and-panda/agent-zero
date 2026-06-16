# Revenue Plan: Agentic Financial System

This plan translates the charter into concrete, compliant execution lanes.

## 1. Principles

- Prefer first-party data over scraped or purchased data.
- Prefer services that can be validated with existing repo assets.
- Prefer short feedback loops and clear monetization paths.
- Reject any lane that fails the compliance pack even if it appears fast to monetize.

## 2. Phase 1 Priority Order

### Priority A: Consent-Based Inbox-to-CRM Hygiene

Why first:

- strong fit with Agent Zero orchestration and RAG
- valuable for small businesses with messy inboxes
- uses owner-authorized data instead of third-party contact harvesting
- can become a recurring retainer

Execution shape:

1. Connect to a client-owned mailbox or export.
2. Retrieve messages via approved API/export.
3. Use RAG to classify threads, organizations, and intent.
4. Extract structured records into a client-owned CRM or CSV.
5. Produce dashboards for warm leads, stale threads, and follow-up priorities.

Use Orange DataScaping only on the approved export or CRM output for clustering, segmentation, and prioritization.

### Priority B: Autonomous Listing Service

Why second:

- already has repo-aligned scaffolding
- produces visible output quickly
- monetization path is simple and concrete

Execution shape:

1. Use the listing microservice scaffold for draft generation.
2. Add pricing intelligence and platform-safe publishing.
3. Instrument response time, sell-through, and margin.

### Priority C: Research and Intelligence Products

Why third:

- low operational risk
- easy to deliver with existing agent/research primitives
- useful hedge while service lanes mature

Execution shape:

1. Offer niche market maps and workflow audits.
2. Package outputs into repeatable briefs and dashboards.
3. Convert repeat demand into subscriptions or retained intelligence.

## 3. Phase 1 Rejections

These do not move forward:

- email list brokerage
- inbox-derived contact resale
- scraping contacts from arbitrary files for sale
- using Gmail RAG to manufacture cold outreach lists

## 4. Activation Checklist

Before a lane goes live:

1. Score it with `instruments/strategy/score.sh`.
2. Confirm it passes legality and consent gates.
3. Define a narrow first customer or internal pilot.
4. Record the experiment in `journal.md`.
5. Add the next improvement hypothesis to `improvements.md`.

## 5. Candidate Offers

### Offer 1: Inbox Cleanup and Revenue Recovery

Deliverables:

- mailbox classification
- warm lead extraction into CRM
- duplicate removal
- dormant thread detection
- suggested follow-up queue

Charging options:

- one-time cleanup
- monthly monitoring
- premium dashboard or SLA support

### Offer 2: Marketplace Listing Concierge

Deliverables:

- photo enhancement
- multi-platform descriptions
- pricing suggestions
- publication workflow

Charging options:

- per item
- bundle package
- subscription for recurring sellers

### Offer 3: Operator Intelligence Brief

Deliverables:

- competitor mapping
- market observations
- price and workflow benchmarking
- recommended next actions

Charging options:

- per report
- monthly subscription

## 6. Near-Term Questions to Answer

- Which first-party inbox or CRM workflow can be piloted with the least setup?
- Which listing categories have the strongest margin and shortest sales cycle?
- Which research niche has the clearest recurring demand?

## 7. Default Decision Rule

If a proposed lane offers fast cash but depends on non-consensual personal data use, reject it and replace it with a compliant first-party variant.
