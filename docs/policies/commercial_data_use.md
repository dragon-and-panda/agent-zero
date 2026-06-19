# Commercial Data Use Policy Pack

This policy pack defines the minimum rules for any Agent Zero workflow that touches contact data, inbox data, CRM exports, or revenue operations.

It is intended to be referenced by autonomous agents, prompt packs, instruments, and human operators before enabling monetization workflows.

---

## 1. Purpose

The goal of this project is to build revenue-generating automation without crossing legal, privacy, or platform-policy boundaries.

That means the system may help with:

- consent-based lead generation
- first-party customer research
- inbox organization for the account owner
- compliant CRM enrichment
- sales operations for lawful B2B outreach

The system must not be used to harvest, package, or sell personal data.

---

## 2. Prohibited Activities

The following uses are disallowed:

1. **Selling or brokering email lists**
   - Do not compile email addresses from mailboxes, scraped pages, or files for resale.
   - Do not market "lead databases" that contain personal email data collected without explicit consent.

2. **Inbox harvesting**
   - Do not extract contact lists from Gmail or other mail systems for monetization.
   - Do not repurpose historical correspondence into a resale dataset.

3. **Unauthorized account access**
   - Do not bypass authentication, scrape private systems, or process data from accounts the operator does not control.

4. **Unconsented personal-data enrichment**
   - Do not merge inbox data, scraped data, and third-party sources to build identity profiles on individuals without a lawful basis.

5. **Spam-oriented workflows**
   - Do not use the framework to generate unsolicited bulk outreach that violates applicable law, mailbox provider terms, or anti-spam rules.

6. **Deceptive monetization**
   - Do not disguise scraped or private-source data as "opt-in" inventory.
   - Do not claim rights to resell data unless those rights are explicit, documented, and auditable.

---

## 3. Allowed Uses

The following uses are generally acceptable when local law, contracts, and platform terms also allow them:

1. **Owner-authorized inbox analysis**
   - Summarize the account owner's own email for tasks like triage, deal tracking, invoice extraction, support routing, or opportunity discovery.

2. **Consent-based audience building**
   - Manage contacts that opted in through forms, newsletters, purchases, referrals, or signed partner agreements.

3. **Public business-contact research**
   - Research business-facing contact points published for commercial communication, subject to site terms, local law, and suppression handling.

4. **CRM hygiene**
   - Deduplicate, score, tag, and route contacts already lawfully held by the operator.

5. **Market intelligence**
   - Analyze demand signals, competitor positioning, public procurement notices, and first-party customer feedback.

---

## 4. Data Classification Rules

Every workflow must classify source data before use:

| Class | Examples | Default Handling |
| --- | --- | --- |
| First-party consented | newsletter signups, customers, demo requests | allowed with purpose limitation |
| Owner mailbox data | the operator's Gmail threads, receipts, support mail | allowed for analysis, not for resale |
| Public business data | published company contact pages, vendor directories | allowed only if terms and law permit use |
| Sensitive or personal data | personal inboxes, private attachments, health/financial data | deny unless there is a clear lawful basis and a narrow use |
| Unknown provenance | CSVs, scraped dumps, inherited lists | quarantine until provenance is proven |

Unknown provenance data should be treated as blocked input until the operator can document where it came from and what rights attach to it.

---

## 5. Gmail and RAG Guardrails

If RAG is used with Gmail or other mailbox data:

- only connect accounts controlled by the operator
- only ingest messages required for the stated business purpose
- store provenance metadata for each document chunk
- support deletion and re-indexing when source messages are removed
- never expose mailbox-derived contacts as a product for sale
- keep retrieval scoped to internal analysis, CRM follow-up, or owner-approved drafting

Recommended safe use cases:

- identify warm inbound leads already requesting information
- summarize recurring customer pain points
- detect unpaid invoices or renewal opportunities
- draft responses for human review

---

## 6. Approved Monetization Patterns

Use the agentic system to sell value, not harvested identities. Safer starting patterns include:

- productized research services
- consent-based outbound appointment setting
- niche content and newsletter businesses
- lead magnets that capture explicit opt-in
- partner prospecting from public business sources
- internal sales-ops automation for your own offers
- micro-SaaS products driven by first-party user workflows

---

## 7. Enforcement Checklist

Before a workflow can run, confirm:

- source ownership or permission is documented
- the business purpose is documented
- resale of personal data is not part of the workflow
- opt-out and deletion handling exist where applicable
- platform terms do not prohibit the collection method
- logs capture provenance, transformations, and outputs

If any item fails, the workflow should stop and escalate.

---

## 8. Default Decision

If a workflow asks to extract email addresses from messages or files and sell them, the answer is **deny**.

Redirect the workflow toward a consent-based revenue model instead.
