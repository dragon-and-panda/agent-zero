# Strategy Intake Queue

Use this queue to normalize new venture ideas before any code, scraping, outreach, or automation begins.

## Intake template

For each idea, capture:

- lane name
- customer or asset owner
- revenue model
- data sources
- consent status
- platform dependencies
- operational risks
- next validation step
- score result from `instruments/strategy/score.sh`

## Current queue

### 1. Inbox-to-CRM assistant

- lane name: Inbox-to-CRM assistant
- customer or asset owner: mailbox owner or client with explicit authorization
- revenue model: setup fee plus monthly retainer
- data sources: Gmail or IMAP messages owned by the client, CRM records, opt-in form submissions
- consent status: acceptable only with explicit owner authorization and defined CRM purpose
- platform dependencies: Google API scopes, CRM API scopes, email-provider terms
- operational risks: over-collection, wrong-field sync, poor deduplication
- next validation step: define minimal sync schema and run the strategy scorer
- score result from `instruments/strategy/score.sh`: expected PASS if provenance and consent are documented

### 2. Autonomous listing service

- lane name: Autonomous listing service
- customer or asset owner: seller controlling the physical inventory
- revenue model: listing fee, managed service fee, or revenue share
- data sources: seller photos, seller notes, marketplace metadata, public comps where permitted
- consent status: acceptable with seller authorization
- platform dependencies: marketplace posting and messaging rules
- operational risks: wrong pricing, platform throttling, returns handling
- next validation step: narrow to one marketplace and one inventory category
- score result from `instruments/strategy/score.sh`: expected PASS or HOLD depending on margins and repeatability

### 3. Research subscription on public data

- lane name: Public-data research subscription
- customer or asset owner: subscribers purchasing analysis
- revenue model: recurring subscription
- data sources: public filings, public web content within allowed access patterns, licensed datasets
- consent status: acceptable because no personal data resale is involved
- platform dependencies: source licenses and API terms
- operational risks: stale data, low differentiation, thin willingness to pay
- next validation step: define a niche and sample deliverable
- score result from `instruments/strategy/score.sh`: expected HOLD until defensibility improves

### Rejected example: personal email list brokerage

- reason for rejection: requires extracting or aggregating personal contact data for resale
- hard gate failure: legality, consent, provenance, and platform-rule compliance
- replacement path: shift to first-party lead capture or inbox-to-CRM automation for a consenting owner
