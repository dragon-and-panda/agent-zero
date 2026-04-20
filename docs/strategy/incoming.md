# Strategy intake queue

Use this queue to screen new monetization ideas before any execution work starts.

## Intake template

- lane:
- customer:
- value proposition:
- acquisition source:
- consent/provenance:
- deliverable:
- automation surface:
- dependencies:
- hard-gate risks:
- notes:

## Active candidates

### 1. Inbox-to-CRM assistant
- lane: compliant inbox triage and CRM enrichment
- customer: operators, founders, solo consultants, agencies
- value proposition: classify inbound email, extract action items, create follow-up drafts, and sync consented contact records into a CRM
- acquisition source: first-party inboxes and user-owned records only
- consent/provenance: explicit user access to the inbox; no third-party list harvesting
- deliverable: service setup, playbooks, dashboards, and managed automations
- automation surface: high
- dependencies: Gmail API or exported mailbox access, CRM destination, prompt/tooling guardrails
- hard-gate risks: privacy compliance, customer data handling
- notes: highest-priority lane because it is legal, useful, and compatible with Agent Zero

### 2. Autonomous listing service
- lane: listing optimization and resale operations
- customer: small ecommerce and marketplace sellers
- value proposition: automate intake, copy generation, enrichment, pricing support, and channel publishing
- acquisition source: client-owned product data and media
- consent/provenance: client-supplied assets and metadata
- deliverable: managed listing operations or software subscription
- automation surface: high
- dependencies: listing service blueprint, storage, channel adapters
- hard-gate risks: marketplace policy compliance
- notes: active hedge with a stronger operational footprint than the inbox lane

### 3. Research product subscriptions
- lane: curated intelligence feeds and lead research packs
- customer: agencies, recruiters, B2B operators
- value proposition: sell market maps, account intelligence, and opt-in prospect research without selling personal data
- acquisition source: public websites, official registries, and client-provided targets
- consent/provenance: public/business context only; no personal inbox scraping
- deliverable: recurring research brief or analyst-on-demand workflow
- automation surface: medium to high
- dependencies: provenance checks, repeatable packaging
- hard-gate risks: terms-of-service limits, data freshness
- notes: attractive if differentiated by speed and packaging
