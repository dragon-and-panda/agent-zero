# Incoming Venture Queue

Use this file to capture new venture ideas before implementation. Every idea should be scored with `instruments/strategy/score.sh` and checked against `docs/policies/compliance_pack.md`.

## Queue template

### Idea
- Summary:
- Customer:
- Monetization:
- Data source:
- Consent basis:
- Platform dependency:
- Automation potential:
- Notes:

### Score
- Status:
- Reasons:
- Next action:

---

## Example: approved direction

### Idea
- Summary: Turn owned or client-owned inventory into polished multi-platform listings and automate inquiry triage.
- Customer: small sellers and local resellers
- Monetization: monthly subscription plus per-listing usage fees
- Data source: first-party inventory data and public marketplace guidance
- Consent basis: seller supplies the content directly
- Platform dependency: medium
- Automation potential: high
- Notes: align with `docs/autonomous_listing_service.md`

### Score
- Status: PASS
- Reasons: first-party data, clear customer value, repeatable workflow
- Next action: prototype pricing and intake workflow

---

## Example: approved inbox-to-CRM direction

### Idea
- Summary: Export owner-authorized or client-authorized mailbox/CRM data with consent markers, dedupe opted-in contacts, analyze segments in Orange, and sync clean records into a CRM.
- Customer: operators, agencies, or support teams working on their own or client-owned relationships
- Monetization: managed service retainer or internal automation product
- Data source: first-party CSV exports with explicit consent or contractual authorization
- Consent basis: existing opted-in relationship or client-approved operational use
- Platform dependency: medium
- Automation potential: medium
- Notes: use `instruments/custom/consent_contact_extract/consent_contact_extract.sh` before Orange analysis or CRM sync

### Score
- Status: PASS
- Reasons: owner-authorized data, clear operational value, bounded use case
- Next action: define export schema, required consent fields, and suppression rules

---

## Example: rejected direction

### Idea
- Summary: Extract email addresses from Gmail and other files, organize them, and sell the compiled lists online.
- Customer: list brokers and cold outreach buyers
- Monetization: one-time list sale
- Data source: private inbox data and ambiguous files
- Consent basis: none
- Platform dependency: high
- Automation potential: high
- Notes: violates privacy, spam, and data-brokerage constraints

### Score
- Status: REJECT
- Reasons: personal-data resale, non-consensual inbox use, high legal and platform risk
- Next action: replace with a first-party opt-in audience, marketplace automation, or an owner-authorized inbox-to-CRM workflow
