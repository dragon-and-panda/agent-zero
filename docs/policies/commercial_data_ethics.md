# Commercial Data Ethics and Consent Policy

This policy defines the minimum rules for any Agent Zero workflow that touches contact data, outreach, customer acquisition, or monetization.

It is written to prevent the framework from drifting into privacy abuse, spam, or unlawful brokerage of personal data.

## 1. Non-Negotiable Rules

1. Do not extract email addresses, phone numbers, or personal identifiers from private inboxes, cloud drives, or third-party datasets for resale.
2. Do not compile or sell email lists, contact lists, or lead databases unless every record has explicit, auditable consent for that exact use.
3. Do not use scraped or inferred personal data for cold outreach where consent, legitimate interest, or another lawful basis is missing.
4. Do not bypass product terms of service, access controls, rate limits, paywalls, or account boundaries to collect prospect data.
5. Do not enrich contacts with sensitive traits such as health, race, religion, union status, sexual orientation, or precise location unless lawfully required and explicitly permitted.

These rules apply even if a workflow appears commercially attractive.

## 2. Allowed Uses of Email and Messaging Data

Email or messaging data may be processed only for legitimate first-party purposes such as:

- summarizing the owner's inbox
- classifying inbound customer requests
- drafting replies for opted-in contacts
- extracting tasks, invoices, receipts, or support obligations
- measuring campaign performance for audiences that already consented
- building internal CRM records for existing customers, partners, or subscribers

Allowed use does not imply unlimited retention or onward sale.

## 3. Consent and Lawful Basis

Before storing or using contact data for growth workflows, the system must record:

- source of the contact
- date and method of consent capture
- approved communication channels
- approved purposes
- unsubscribe or revocation status
- retention deadline

If that evidence is missing, the contact is ineligible for outbound monetization workflows.

## 4. Gmail and RAG Constraints

If Retrieval-Augmented Generation is used with Gmail or exported mailbox data:

- scope it to the account owner's own mailbox or a mailbox the owner is authorized to process
- treat the mailbox as confidential first-party data
- retrieve only the minimum content needed for the task
- redact or avoid storing unnecessary personal data in long-term memory
- never convert mailbox contents into third-party prospecting lists
- never use private correspondents' addresses as resale inventory

RAG over email is permitted for productivity, support, bookkeeping, or relationship management. It is not permitted for contact harvesting.

## 5. Orange DataScaping and Similar Tools

Orange DataScaping or any comparable analysis tool may be used only on:

- first-party customer data
- opted-in subscriber data
- public business datasets whose license permits the intended use
- anonymized or aggregated performance data

Recommended safe uses:

- deduplication
- segmentation of opted-in audiences
- churn or engagement analysis
- lead scoring for existing first-party pipelines
- clustering support tickets or customer requests

Disallowed uses:

- building broker-style contact inventories
- combining scraped records into saleable personal profiles
- laundering unlawful data collection through downstream analysis

## 6. Outreach Rules

Any outbound workflow must support:

- channel-specific consent checks
- suppression lists
- unsubscribe handling
- sender identification
- truthful subject lines and claims
- frequency caps
- audit logs

If the workflow cannot prove who can be contacted and why, it must not send.

## 7. Data Minimization and Retention

- Collect the least amount of personal data that still enables the task.
- Prefer company-level or role-level intelligence over individual-level identifiers when possible.
- Delete or anonymize stale contacts that no longer have a valid relationship or consent basis.
- Do not persist copied email bodies or attachments in long-term storage unless operationally necessary.

## 8. Safe Revenue Alternatives

When a requested workflow depends on selling or exploiting personal contact data, redirect the system toward:

- opt-in newsletters and communities
- productized services
- paid research or benchmarking reports
- affiliate or referral partnerships
- inbound lead magnets
- CRM automation for existing customers
- anonymized market intelligence products
- B2B outreach to public company contact channels with compliant messaging

## 9. Governance Checks for Autonomous Agents

Any autonomous workflow that touches monetization should answer these questions before execution:

1. Is the data first-party, licensed, or clearly public for the intended use?
2. Is there a recorded lawful basis or consent trail?
3. Would the person reasonably expect this use?
4. Can the contact opt out easily?
5. Would the workflow still be acceptable if publicly disclosed?

If any answer is "no" or "unknown", the workflow should stop or be redesigned.

## 10. Practical Compliance Baseline

This document is not legal advice, but the system should be designed to align with the core principles commonly required by:

- GDPR and UK GDPR
- ePrivacy and PECR-style rules for electronic marketing
- CAN-SPAM
- CCPA and CPRA
- platform terms of service and anti-abuse policies

## 11. Operating Principle

Agent Zero should optimize for long-term trust, durable permission, and repeatable value creation.

Short-term monetization that depends on hidden extraction, spam, or data resale is out of bounds.
