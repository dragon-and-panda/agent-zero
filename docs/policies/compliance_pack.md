# Compliance Pack for Autonomous Revenue Programs

This policy pack governs any autonomous workflow in this repository that touches:

- personal data,
- outreach or sales activity,
- third-party platforms,
- payments, treasury, or speculative finance.

The goal is simple: build durable revenue through legal, ethical, auditable means. If a proposed workflow conflicts with this document, the workflow is out of scope until it is redesigned.

---

## 1. Hard prohibitions

The system must not:

1. Buy, sell, rent, or broker email lists or other personal contact data.
2. Extract contact data from inboxes, files, or websites for resale, spam, or unauthorized outreach.
3. Scrape, access, or export private account data without explicit authorization from the account owner and a documented business purpose.
4. Send bulk unsolicited outreach that violates platform rules, anti-spam laws, or recipient expectations.
5. Circumvent paywalls, access controls, CAPTCHAs, rate limits, or anti-abuse protections in ways that violate terms of service or law.
6. Misrepresent identity, affiliation, product performance, pricing, or availability.
7. Process regulated financial activity without the required licensing, disclosures, and controls.
8. Place operating capital into leveraged trading or high-volatility speculation without explicit capital-allocation gates defined in the mission charter.

Any plan built around private-data resale, mailbox harvesting for list sales, or platform abuse is automatically rejected.

---

## 2. Approved use of communications data

Mailbox and communications data may be used only in the following narrow cases:

1. The data belongs to the user or their organization, and the user has authorized the processing.
2. The use case is internal relationship intelligence, customer support, supplier management, CRM hygiene, or knowledge retrieval.
3. Outputs remain first-party and are not sold, rented, or shared outside the authorized business purpose.
4. Each contact record carries:
   - provenance,
   - consent or relationship status,
   - retention window,
   - suppression or opt-out state.

Approved examples:

- Indexing a first-party mailbox with RAG so the system can answer "Which suppliers replied last month?" or "What are the recurring customer complaints?"
- Extracting counterparties from sent and received mail to build a private CRM for follow-up, provided the data is not repurposed into cold-list sales.
- Using Orange Data Mining or similar tools to segment first-party contacts by relationship stage, activity, or product interest.

Disallowed examples:

- Building a sellable list of email addresses from private mailboxes.
- Reusing old contacts for marketing when there is no consent, no lawful basis, or an opt-out exists.
- Enriching personal contact data with scraped details for resale or mass outreach.

---

## 3. Outreach and demand generation rules

Allowed acquisition channels:

- inbound forms,
- opt-in newsletters,
- marketplace demand,
- referral programs,
- affiliate programs,
- partnerships,
- public content,
- one-to-one outreach to relevant businesses where the message is contextual, compliant, and logged.

All outbound workflows must:

1. maintain suppression lists,
2. honor opt-outs promptly,
3. include truthful sender identity,
4. avoid deceptive subject lines or claims,
5. stay within channel-specific sending limits and policies,
6. log the reason the recipient was selected.

The default preference is owned-audience growth over cold outreach.

---

## 4. Platform and automation rules

Automation may assist with publishing, analysis, and operations, but it must not depend on abusive platform behavior.

Required controls:

- respect robots, rate limits, and published API rules,
- prefer official APIs over fragile or adversarial browser automation,
- use human fallback instead of anti-bot circumvention when a platform blocks automation,
- log platform-specific compliance notes before launch.

If platform automation requires breaking terms of service, the workflow must be redesigned or abandoned.

---

## 5. Revenue model allowlist

The following monetization patterns are in scope:

- productized services,
- marketplace listing optimization,
- consulting or implementation retainers,
- software subscriptions,
- digital products and templates,
- courses and educational content,
- affiliate revenue,
- compliant lead generation based on opt-in or marketplace intent,
- first-party data intelligence products that do not expose private personal data.

The following patterns are out of scope:

- selling harvested contact data,
- spam-driven arbitrage,
- fake engagement or fake reviews,
- account farming,
- fraudulent trading schemes,
- undisclosed paid promotion,
- any revenue source that depends on platform abuse or deceptive identity.

---

## 6. Treasury and capital allocation policy

Revenue must be handled as documented business income with basic bookkeeping and tax records.

Capital rules:

1. Keep an operating reserve before funding experimental bets.
2. Reinvest only after unit economics and delivery quality are measured.
3. Treat speculative trading as a sandboxed research sleeve, not the core engine of the business.
4. Do not risk payroll, taxes, vendor obligations, or core operating cash on trading.
5. Owner distributions may be routed to approved personal accounts only after the revenue is documented, reconciled, and legally earned.

---

## 7. Trading-specific guardrails

If a mission includes market trading research:

- start with paper trading,
- define explicit max drawdown and position-size limits,
- restrict live deployment to a small experimental sleeve,
- separate research capital from operating capital,
- maintain a written stop condition,
- never market the activity as guaranteed or "most profitable."

The system should favor stable cashflow businesses first and treat trading as an optional later-stage research program.

---

## 8. Audit requirements

Every autonomous revenue workflow must keep a minimal audit trail:

- mission owner,
- objective,
- data sources,
- consent status or lawful basis,
- tools used,
- outputs produced,
- revenue generated,
- incidents or policy exceptions.

If the system cannot explain where data came from or why a person was contacted, the workflow fails audit.

---

## 9. Release checklist

Before launching a new revenue workflow, confirm:

- [ ] The workflow does not sell or expose private personal data.
- [ ] Data provenance is documented.
- [ ] Consent, relationship basis, or marketplace intent is recorded where needed.
- [ ] Platform terms and rate limits have been reviewed.
- [ ] Financial downside is capped.
- [ ] A fallback plan exists if the primary channel is disabled.
- [ ] Logging and review hooks are enabled.

This file is the canonical policy bundle referenced by the Compliance Guardian in `docs/autonomous_super_agency.md`.
