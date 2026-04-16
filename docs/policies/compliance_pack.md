# Compliance Pack for the Agentic Financial System

This pack defines the minimum operating rules for any revenue workflow built on top of Agent Zero.

## 1. Mission Boundary

The system may only pursue ethical, legal, and consent-based revenue.

Out of bounds:
- scraping, brokering, buying, compiling, or selling personal email lists or contact databases
- using Gmail, IMAP, or other inbox access without the account owner's explicit authorization
- sending cold outreach to scraped, purchased, or otherwise non-consensual recipients
- bypassing platform terms of service, anti-bot controls, CAPTCHA challenges, or rate limits for prohibited actions
- storing personal data longer than operationally necessary

## 2. Approved Revenue Lanes

Allowed lanes include:
- first-party newsletter growth using explicit opt-in forms and double opt-in where practical
- client-owned CRM cleanup, tagging, and segmentation for contacts the client lawfully collected
- owner-authorized inbox triage, RAG, and CRM drafting for existing business relationships
- marketplace listing services and other workflow automation that operate on the client's own assets
- research, benchmarking, and data products built from public, licensed, synthetic, or anonymized aggregate data
- audience access products such as newsletters, communities, or sponsorship inventory where subscribers knowingly opted in

## 3. Hard Gates

Every proposed lane must pass all of these gates before any build or activation work begins:

1. Legality
   - The workflow is lawful in the target jurisdiction.
   - The workflow does not require trafficking in personal data.
2. Consent
   - The people whose data is used knowingly opted in, or the client has another valid and documented basis to process it.
3. Data provenance
   - The source of each dataset is known, documented, and reproducible.
4. Platform terms
   - The workflow does not depend on violating third-party terms or abuse-prevention systems.

If any hard gate fails, the lane is rejected.

## 4. Gmail and RAG Rules

Inbox-based workflows are allowed only when all of the following are true:
- the account owner or authorized client explicitly requested the workflow
- access is scoped to the minimum mailbox surface needed for the task
- retrieved content is used to support internal triage, summarization, drafting, CRM updates, or support operations
- sensitive content is masked or excluded when it is not required
- audit logs record who authorized access, when the sync happened, and what downstream systems received derived data

Inbox content may not be used to build third-party contact lists for resale.

## 5. Orange-Based Data Analysis Rules

Orange or similar data-mining tooling may be used for:
- deduplication
- segmentation
- lead scoring on first-party consented records
- clustering on anonymized or aggregate datasets

Orange may not be used to operationalize scraped personal data or prepare non-consensual lists for outreach or sale.

## 6. Data Handling Standards

- Collect the minimum fields needed for the active workflow.
- Separate raw personal data from derived analytics.
- Encrypt secrets and private exports at rest and in transit.
- Define retention windows and deletion procedures before production use.
- Prefer hashed, aggregated, or anonymized outputs whenever the business model does not require direct identifiers.

## 7. Replacement Patterns for Rejected Ideas

Rejected pattern:
- "Compile email addresses and sell the list."

Compliant replacements:
- build an opt-in lead magnet funnel and monetize through services, sponsorships, or subscription access
- clean and enrich a client's existing lawful CRM, then sell the workflow as a managed service
- produce market intelligence from public or licensed data and sell the report, not the personal contacts
- create a marketplace automation or listing concierge service and charge for outcomes or retained automation

## 8. Required Repo Artifacts

Each active lane should reference:
- `docs/policies/compliance_pack.md`
- `docs/strategy/incoming.md`
- `docs/programs/agentic_financial_system/charter.md`
- `docs/programs/agentic_financial_system/journal.md`
- `docs/programs/agentic_financial_system/improvements.md`
- `instruments/strategy/score.sh`

## 9. Stop Conditions

Pause and escalate if:
- the workflow depends on unclear consent
- the data source cannot be proven
- a platform blocks or forbids the automation
- the plan drifts toward personal-data resale, spam, or deceptive acquisition
