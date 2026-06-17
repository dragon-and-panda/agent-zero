# Compliance Pack: Autonomous Revenue Operations

This policy pack governs any Agent Zero workflow that touches monetization, customer data, outreach, inbox content, or external platforms.

## Hard-stop prohibitions

Do not:

- sell, rent, or broker personal email addresses or contact lists
- scrape inboxes, CRMs, cloud drives, or documents without the owner's explicit authorization
- generate spam, mass unsolicited outreach, or platform-evasion playbooks
- hide automation in ways that violate platform rules or anti-abuse systems
- use purchased, scraped, leaked, or ambiguously sourced personal data
- help users bypass privacy, consent, identity, or anti-spam controls

## Allowed uses of contact and inbox data

Allowed only when all of the following are true:

1. The operator owns the account or has explicit written authorization.
2. The use is consistent with documented consent and the intended purpose.
3. The workflow is first-party, service-delivery, support, analytics, or CRM hygiene related.
4. The minimum necessary data is processed and retained.

Examples of allowed use:

- deduplicating an owner-authorized newsletter list
- summarizing a founder's inbox to identify support themes
- tagging inbound leads that opted into contact
- extracting customer-service issues from first-party mail for routing

## Required decision gates

Before executing a monetization workflow, check:

- Legality: is the workflow lawful in the operating jurisdiction?
- Consent: do the relevant people expect and permit this use?
- Provenance: is the data first-party, licensed, or clearly authorized?
- Platform risk: does the target platform allow the behavior?

If legality or provenance fails, return REJECT.
If consent or platform rules are unclear, return HOLD.

## Preferred alternatives to prohibited requests

When asked to monetize by using personal contact data in unsafe ways, redirect toward:

- opt-in newsletter growth
- productized services
- first-party CRM cleanup
- anonymized analytics products
- seller-authorized commerce automation
- content, software, and subscriptions

## Audit expectations

Every approved workflow should leave an audit trail describing:

- objective
- data source
- authorization basis
- consent status
- platform touched
- decision outcome: PASS, HOLD, or REJECT
