# Agentic Financial System Charter

## Mission

Build a self-sustaining financial system around Agent Zero that generates revenue through ethical, lawful, automation-friendly products and services with minimal human supervision.

## Non-Negotiable Constraints

- no personal-data resale
- no non-consensual inbox mining
- no deceptive or spam-first acquisition loops
- no workflows that depend on violating platform terms

The compliance baseline lives in `docs/policies/compliance_pack.md`.

## Operating Principles

1. Sell outcomes, not harvested data.
2. Prefer first-party or client-owned data over third-party datasets.
3. Default to opt-in acquisition and service delivery with obvious customer value.
4. Treat automation as a margin multiplier, not a reason to weaken consent or governance.
5. Score every new lane before activation.

## Phase 1 Revenue Lanes

### 1. Inbox-to-CRM Assistant
- Customer: founders, small teams, agencies
- Offer: convert owner-authorized inboxes into triaged tasks, CRM entries, and follow-up drafts
- Why it fits: high utility, clear consent boundary, recurring revenue potential

### 2. Autonomous Listing Operations
- Customer: resellers, local businesses, side hustlers
- Offer: create, publish, optimize, and manage marketplace listings
- Why it fits: adjacent to existing repo assets under `services/autonomous_listing/`

### 3. Research and Market Intelligence Products
- Customer: operators who need niche market maps, lead magnets, or competitor tracking
- Offer: recurring briefs, data-backed insights, and playbooks built from lawful sources
- Why it fits: strong automation fit without reselling personal data

### 4. Agent Workflow Audits and Implementations
- Customer: small businesses adopting AI automation
- Offer: audit repetitive work, implement safe agent workflows, and maintain them on retainer
- Why it fits: high-margin service lane that compounds repository value

## Lanes Explicitly Rejected

- selling compiled email lists
- extracting contact databases from Gmail or local files for third-party monetization
- brokering scraped inbox data to marketing platforms

## Decision Process

For every candidate lane:

1. record it in `docs/strategy/incoming.md`
2. run the hard-gate and soft-factor screen with `python/tools/revenue_planning.py`
3. verify the same decision with `instruments/strategy/score.sh`
4. activate only if the lane passes compliance and has acceptable attractiveness

## Core Metrics

- compliant revenue generated
- time to first value for customers
- gross margin
- repeatability of delivery
- percent of workflows that remain human-light after onboarding
- number of active lanes passing hard compliance gates

## Near-Term Build Priorities

1. restore the compliance and planning scaffold in-repo
2. harden prompts so the agent rejects privacy-invasive monetization schemes
3. turn the inbox-to-CRM lane into a client-owned workflow, not a data-broker workflow
4. keep the Autonomous Listing Service as an adjacent revenue hedge
