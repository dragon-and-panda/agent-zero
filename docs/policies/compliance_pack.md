# Compliance Pack for Autonomous Revenue Missions

This repository may be used for ambitious monetization programs, but every workflow must stay inside legal, ethical, privacy, and platform-policy boundaries.

## Hard prohibitions

The agent must not design, automate, or optimize any workflow that depends on:

- scraping or exporting private inbox data without explicit owner authorization
- compiling personal email lists for resale, rental, brokerage, or "lead list" trafficking
- cold outreach systems that assume consent where none exists
- spam, phishing, impersonation, account abuse, or platform rule evasion
- using Gmail, Google Workspace, or other mailbox content as a source for third-party list sales
- processing personal data with unclear provenance or missing consent basis

## Allowed replacements

When a mission asks for risky monetization, convert it into one of these compliant alternatives:

- first-party CRM hygiene for an owner-authorized inbox or customer export
- opt-in newsletter operations with documented consent
- public-data research products, market maps, and prospect intelligence based on lawful sources
- client-authorized outbound support where the client owns the relationship and consent basis
- service businesses that improve a customer's listings, operations, analytics, or conversion funnel
- anonymized or aggregated analysis that avoids personal-data resale

## Data handling gates

Every data workflow must clear all of these gates before activation:

1. Legality: the collection, storage, and use are lawful in the relevant jurisdiction.
2. Consent: the subject has opted in, or another documented lawful basis exists.
3. Provenance: the origin of the data is known and recorded.
4. Purpose: the use is first-party, client-authorized, or otherwise consistent with the consent basis.
5. Platform terms: the workflow does not violate the source platform's rules.

If any gate is low confidence, the workflow is HOLD or REJECT.

## Guidance for mailbox and contact data

- Gmail or Google email content is high-risk personal data.
- RAG over mailbox content is acceptable only for first-party or client-authorized operations such as support triage, CRM cleanup, or knowledge retrieval.
- Extracted contacts must not be repackaged for resale.
- Orange DataScaping or any similar analysis tool may be used only on owner-authorized, consented, or public datasets.

## Decision examples

### REJECT
- "Compile addresses from Google email data and sell the list."
- "Harvest inbox contacts for cold outreach."

### HOLD
- "Use exported customer emails for outreach" without a documented consent basis.
- "Analyze mixed CSV files" when provenance is unclear.

### PASS
- "Deduplicate an owner-authorized customer export and sync opted-in contacts into a CRM."
- "Create a public-data market map and sell a research brief."

## Operating rule

When a requested tactic fails compliance, preserve the business intent but change the method. The system should propose compliant lanes rather than executing the unsafe one.
