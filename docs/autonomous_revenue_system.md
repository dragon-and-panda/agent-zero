# Autonomous Revenue System

This guide translates high-autonomy business-building goals into a compliant operating model for Agent Zero.

## Mission

Build a self-sustaining revenue engine that:

- uses autonomous research, planning, and execution loops
- stays inside legal, ethical, and platform-compliant boundaries
- uses inbox and customer data only with clear owner authorization
- monetizes services, software, or research instead of personal-data resale

## Explicit non-goals

The system must not:

- extract email addresses from Gmail or other inboxes to create brokerage lists
- sell, rent, or trade personal contact data
- run bulk unsolicited outreach or spam-like campaigns
- use Orange or any other analytics tool to process scraped or bought contact lists

Those paths are blocked by `docs/policies/compliance_pack.md` and by the `revenue_planning` guardrail tool.

## Safe system architecture

### 1. Intake and scoring

Capture ideas in `docs/strategy/incoming.md`, then score them with:

- `instruments/strategy/score.sh`
- `python/tools/revenue_planning.py`

Only ideas that pass legality, consent, provenance, and platform checks should move forward.

### 2. Owner-authorized email RAG

Gmail or email RAG is allowed only for productivity tasks such as:

- summarizing threads
- extracting tasks and commitments
- drafting replies
- routing messages into CRM or project systems
- identifying recurring pain points that can become products or services

Do not use inbox RAG to build resale contact inventories or cold-outreach lists.

### 3. Consent-only contact processing

If a workflow needs contact data, use only first-party or client-authorized exports with explicit marketing permission. Filter them through:

- `instruments/custom/consent_contact_extract/consent_contact_extract.py`

The extractor keeps only rows that show:

- valid consent state
- marketing permission
- acceptable provenance

It rejects inbox-derived, scraped, or purchased provenance.

### 4. Orange-based analysis

Orange Data Mining or similar analytics tools may be used for:

- clustering customer pain points
- segmenting opt-in audiences
- analyzing anonymized support or usage exports
- ranking opportunities from compliant datasets

Orange should only receive:

- anonymized data, or
- authorized first-party/customer data with documented consent and provenance

## Phase 1 monetization lanes

The system should prioritize these low-risk, revenue-capable lanes:

### A. Productized automation service

Sell audits, workflow mapping, and implementation for small teams.

- inputs: client-approved workflow docs, inbox summaries, authorized CRM exports
- revenue: fixed-fee audit plus recurring support
- advantage: monetizes expertise, not personal data

### B. Inbox productivity assistant

Offer an owner-authorized assistant that:

- summarizes inbound email
- extracts action items
- drafts responses
- updates CRM or ticketing systems

Revenue model:

- subscription
- setup fee
- managed operations add-on

### C. Opt-in research and newsletter products

Turn recurring market or operations insights into:

- paid briefings
- premium newsletters
- niche reports
- templates and playbooks

Acquisition model:

- lead magnets
- referrals
- webinars
- opt-in landing pages

### D. Client-authorized CRM hygiene

Provide consent-aware cleanup and enrichment for existing customer records.

- deduplicate records
- flag missing consent
- segment opted-in contacts
- prepare compliant follow-up workflows

## Recommended operating loop

1. Add a candidate idea to `docs/strategy/incoming.md`.
2. Score it with `instruments/strategy/score.sh`.
3. Run the plan through `revenue_planning`.
4. If the plan touches contacts, filter inputs with `consent_contact_extract.py`.
5. Use Orange only on anonymized or consent-cleared datasets.
6. Launch a service, subscription, or research product.
7. Record results in `docs/programs/agentic_financial_system/journal.md`.

## Suggested first execution sequence

Start with this sequence instead of email-list resale:

1. build a productized automation audit offer
2. create an opt-in landing page and lead magnet
3. use owner-authorized inbox RAG to identify repeatable service opportunities
4. deliver CRM cleanup or workflow automation for authorized clients
5. convert successful service patterns into templates, reports, or software

## Success criteria

Track:

- number of scored ideas
- number of PASS / HOLD / REJECT decisions
- opt-in lead growth
- conversion from audit to recurring service
- monthly recurring revenue from compliant offers
- percentage of workflows with documented consent and provenance

## Related files

- `docs/policies/compliance_pack.md`
- `docs/programs/agentic_financial_system/charter.md`
- `docs/strategy/incoming.md`
- `instruments/strategy/score.sh`
- `instruments/custom/consent_contact_extract/consent_contact_extract.py`
- `python/tools/revenue_planning.py`
