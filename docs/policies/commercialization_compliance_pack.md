# Commercialization Compliance Pack

This policy pack governs any Agent Zero workflow that touches revenue generation, customer communications, inbox analysis, prospecting, or market research.

It is an operational policy document, not legal advice. When local law, platform rules, contract terms, or regulatory guidance are stricter than this document, the stricter rule wins.

---

## 1. Purpose

Ensure the commercialization system remains:

- lawful,
- ethical,
- consent-aware,
- platform-compliant,
- and safe for long-term operation.

---

## 2. Core Rules

### Rule 1: Lawful basis and authorization

Only process data when at least one of the following is true:

- the operator owns the mailbox, file, or account,
- the data subject opted in,
- the operator has a contractual right to process the data,
- the data is public business information being used in a narrow, relevant, policy-compliant manner.

If the workflow cannot explain why it is allowed to access or use the data, the workflow must stop.

### Rule 2: No contact-data brokerage

The system must not:

- compile email lists for sale,
- sell, rent, or trade contact data,
- package inbox-derived contacts as a product,
- enrich personal identities for third-party marketing.

Any task whose main output is a transferable contact list is non-compliant.

### Rule 3: Inbox analysis is for operations, support, and conversion

Business inboxes may be analyzed to:

- summarize conversations,
- classify intent,
- detect opportunities,
- draft responses,
- track pipeline state,
- improve products and documentation.

Business inboxes may not be used to create speculative outreach databases.

### Rule 4: Data minimization

Collect and retain the minimum information needed for the workflow.

Preferred order:

1. Aggregated metrics
2. Thread summaries
3. Structured tags
4. Raw content only when necessary

Avoid embedding unnecessary PII, sensitive categories, or entire raw mailboxes when summaries will work.

### Rule 5: Outreach must be specific and compliant

Outbound communication must be:

- relevant,
- individualized or narrowly targeted,
- truthful,
- easy to opt out of,
- consistent with platform rules and applicable law.

The system must not automate spam or mass unsolicited outreach.

### Rule 6: Recordkeeping

For each revenue workflow, store:

- data source,
- purpose,
- output type,
- responsible agent/persona,
- approval path,
- suppression/deletion rules,
- KPI results,
- compliance decision if reviewed.

### Rule 7: Human escalation triggers

Escalate before proceeding when:

- the task mentions scraping, resale, or list building,
- the workflow touches sensitive personal data,
- the relevant law or platform policy is unclear,
- high-value offers require non-standard claims or promises,
- the system cannot determine whether consent exists.

---

## 3. Allowed vs. Disallowed Activities

### Allowed

- Summarizing first-party customer emails
- Building a FAQ corpus from support threads
- Segmenting opted-in leads with Orange Data Mining
- Turning recurring inbound requests into a service offering
- Researching public pricing pages and competitors
- Drafting a response to a qualified inbound prospect

### Disallowed

- Export every address from Gmail into a CSV for resale
- Scrape directories or social platforms for personal emails
- Buy lists and enrich them with inbox data
- Create mass-campaign targets from private correspondence
- Misrepresent identity, affiliation, or intent in outreach

---

## 4. Workflow Preflight Checklist

Before any commercialization workflow runs, answer:

1. What is the business purpose?
2. What data source is being used?
3. Do we own or have consent/authorization for it?
4. Is the output a service/product insight or a contact database?
5. Are we minimizing PII?
6. Is there an unsubscribe, suppression, or deletion path if messaging is involved?
7. Does any step require human review?

If questions 3 or 4 fail, the workflow must stop.

---

## 5. Gmail/RAG Guardrails

When using Gmail or Google Workspace data:

- ingest only approved mailboxes,
- prefer summaries and tags over raw retention,
- separate semantic retrieval content from identity fields,
- redact secrets, credentials, and irrelevant personal details where practical,
- do not treat sender addresses as monetizable inventory,
- honor deletion requests and account disconnects.

---

## 6. Orange Data Mining Guardrails

Orange may be used for clustering, ranking, and visualization only on:

- first-party business data,
- consented customer/prospect data,
- or anonymized operational datasets.

Orange may not be used to operationalize harvested or purchased contact lists.

---

## 7. Platform Policy Guardrails

For marketplaces, email providers, CRMs, and directories:

- respect rate limits and anti-spam rules,
- follow listing/content policies,
- keep claims substantiated,
- avoid scraping where prohibited,
- preserve audit trails for account actions.

When a platform exposes a native workflow for engagement, prefer that over extracting contacts off-platform.

---

## 8. Enforcement Model

Recommended enforcement in Agent Zero:

- **Compliance Guardian:** blocks non-compliant tasks at planning time
- **Budget Guard:** stops low-margin experimentation from running indefinitely
- **Telemetry Sentinel:** flags unusual spikes in sends, exports, or data volume
- **Knowledge Librarian:** ensures reusable SOPs reference the latest approved policy

---

## 9. Default Decision

If the system is unsure whether a commercialization action is permissible, the default action is:

**Do not proceed. Reduce scope, remove personal data, or escalate for review.**
