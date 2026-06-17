# Agentic Financial System Charter

## Mission
Build a self-sustaining, autonomy-friendly revenue system that compounds through lawful software, services, and first-party data operations.

The system must maximize:

- legality and ethical durability,
- repeatable value creation,
- low-touch operation,
- documented learning loops,
- positive unit economics.

It must not rely on:

- brokering personal data,
- extracting or selling email lists,
- unauthorized scraping of private systems,
- deceptive outreach,
- unclear ownership or consent.

## Problem Statement
The original mission aimed for autonomous revenue growth but included a request to extract and sell email lists. That pathway is disallowed by the repository compliance pack and is technically fragile, legally risky, and reputationally destructive.

This program replaces that path with compliant lanes that can still generate revenue with high automation leverage.

## Approved Phase-1 Revenue Lanes

### Lane A: Inbox-to-CRM operations for account owners
- Input: client-owned inbound email or lead data.
- Offer: summarize, classify, route, enrich, and synchronize inbound requests into a CRM or action queue.
- Revenue model: service retainers, usage-based automation fees, or packaged workflow setup.
- Constraint: only first-party or explicitly authorized client-owned inboxes.

### Lane B: Research products
- Input: lawful public/licensed sources.
- Offer: market maps, benchmarks, competitor trackers, or niche intelligence packs.
- Revenue model: subscriptions, one-off reports, or upsell into consulting/services.
- Constraint: maintain provenance and avoid unlicensed datasets.

### Lane C: Listing and commerce automation
- Input: seller-owned product/media data.
- Offer: listing generation, marketplace publishing assistance, inquiry triage, pricing support.
- Revenue model: per-listing fee, subscription, or transaction support retainer.
- Constraint: obey marketplace rules and platform-specific limits.

### Lane D: Opt-in acquisition systems
- Input: owned content, tools, calculators, newsletters, directories.
- Offer: pages and products that attract voluntary signups.
- Revenue model: sponsorships, premium content, SaaS, or service upsells.
- Constraint: store proof of consent and acquisition source.

## Evaluation Criteria
Each lane is scored with `instruments/strategy/score.sh` using:

- legality,
- consent/provenance,
- TOS compatibility,
- evidence of demand,
- reserves/risk readiness,
- time-to-cash,
- margin,
- repeatability,
- automation fit,
- defensibility.

## Initial Prioritization
1. Inbox-to-CRM operations
2. Research products
3. Listing automation
4. Opt-in acquisition systems

Rationale:
- fastest path to lawful value,
- strong fit with existing agent/RAG architecture,
- low need for new regulated infrastructure,
- avoids dependence on third-party personal-data resale.

## Success Metrics

### Commercial
- first revenue-producing lane activated,
- recurring revenue from at least one compliant workflow,
- positive gross margin on automated runs,
- reduced manual intervention per delivery cycle.

### Operational
- every active lane has a journal and improvement backlog,
- every lane passes the strategy score gate before activation,
- every data workflow has provenance and retention notes,
- no active workflow violates the compliance pack.

### Learning
- new reusable prompts, instruments, or playbooks are documented,
- failed lanes are explicitly retired with reasons,
- successful lanes are converted into repeatable SOPs.

## Non-Goals
- selling personal contact databases,
- high-volume cold email based on scraped contacts,
- unlicensed data resale,
- speculative autonomous trading without dedicated controls,
- any workflow whose legality or consent model is ambiguous.

## Operating Cadence
1. Capture candidate lanes in `docs/strategy/incoming.md`.
2. Score each lane with `instruments/strategy/score.sh`.
3. Promote only PASS or justified HOLD candidates into experiments.
4. Log all decisions in `journal.md`.
5. Rank next actions in `improvements.md`.
