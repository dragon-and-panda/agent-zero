# Compliance Pack for Autonomous Revenue Systems

This pack defines the minimum legal, privacy, and platform-compliance rules for any monetization workflow run by Agent Zero or its subordinate agents.

## 1. Purpose

The mission is to build a self-sustaining financial system through lawful, ethical, and auditable online ventures. Revenue does not justify violating consent, privacy, platform terms, or anti-spam laws.

## 2. Hard Prohibitions

The following workflows are disallowed and must be rejected at intake:

- Compiling, brokering, renting, or selling personal email lists or contact databases.
- Extracting email addresses from Gmail, documents, or other files for third-party resale or cold-list building.
- Using inbox access to collect contacts who did not explicitly opt in to outreach.
- Sending unsolicited bulk outreach that would violate CAN-SPAM, GDPR, PECR, CASL, or similar laws.
- Scraping personal data from websites, social networks, or marketplaces in ways that violate terms of service.
- Circumventing anti-bot, CAPTCHA, rate-limit, or access controls for lead harvesting.
- Feeding Orange DataScaping, spreadsheets, vector stores, or RAG pipelines with unlawfully obtained personal data.

## 3. Approved Revenue Patterns

These patterns are allowed when they are documented, consent-based, and compliant with platform rules:

- First-party inbox assistants for the account owner, such as summarization, labeling, routing, and reply drafting.
- Client-owned CRM enrichment using contacts the client already lawfully collected and is permitted to process.
- Opt-in lead magnets, newsletters, waitlists, and other consent-based audience acquisition systems.
- Marketplace listing services, digital products, research reports, affiliate content, and other non-personal-data products.
- Internal RAG over first-party documents for operations, support, and sales enablement.

## 4. Data Handling Rules

Before any workflow touches user data, it must satisfy all of the following:

1. **Legality:** The processing purpose is lawful in the target jurisdiction.
2. **Consent or authority:** The operator owns the mailbox or dataset, or has explicit permission to process it.
3. **Provenance:** The data source is documented and can be traced.
4. **Platform compliance:** The workflow complies with the source platform's terms.
5. **Purpose limitation:** Data is used only for the stated workflow, not repurposed into resale inventory.
6. **Deletion path:** Contacts and source records can be removed or excluded on request.

## 5. Orange DataScaping Usage

Orange DataScaping may be used only as an analysis and organization layer for:

- first-party inbox summaries,
- consented CRM exports,
- internal support or sales triage,
- market research datasets that do not expose personal contact details.

It must not be used to construct or package raw contact lists for sale.

## 6. Intake Gate

Every new monetization lane must pass the scoring instrument in `instruments/strategy/score.sh`.

Any lane must be rejected immediately if any hard gate fails:

- legality,
- consent,
- data provenance,
- platform terms compliance.

## 7. Default Safe Substitutions

When a request is rejected because it depends on personal-data resale or spam, convert it into one of these replacements:

- build an opt-in lead capture funnel,
- build an inbox-to-CRM assistant for first-party operations,
- build a listing or arbitrage workflow that monetizes products rather than contacts,
- build a research product or affiliate content engine,
- build a client service around lawful automation rather than data brokerage.

## 8. Audit Note

If a future prompt asks for email harvesting or contact-list resale, the correct behavior is to refuse that portion and proceed only with the compliant substitutes above.
