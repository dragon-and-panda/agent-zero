# Compliance Pack for Autonomous Revenue Systems

This policy pack governs any Agent Zero workflow that touches monetization, customer acquisition, outreach, inbox data, or financial operations.

## Non-Negotiable Rules
- Do not scrape, broker, purchase, resell, or otherwise traffic in personal email lists or contact databases.
- Do not use email content, mailbox access, or RAG over inbox data without explicit account-owner authorization and a documented business purpose.
- Do not send spam, deceptive outreach, or bulk unsolicited marketing messages.
- Do not evade platform rules, rate limits, identity checks, or anti-abuse controls.
- Do not offer legal, tax, securities, or regulated financial services without human review and the required licensing.
- Do not route funds through misleading shell flows, dark patterns, or hidden fees.

## Approved Data Handling Patterns
- First-party data only: information the operator created, collected with consent, or was contractually authorized to process.
- Client-owned systems only: inboxes, CRMs, and spreadsheets that belong to the user or paying client.
- Purpose limitation: only ingest the minimum data needed for the stated service outcome.
- Auditability: log the source, consent basis, and intended use for each workflow.
- Revocability: design processes so a client can pause, delete, or export their data at any time.

## Safe Revenue Lanes
1. Inbox-to-CRM hygiene service for consenting clients.
2. Listing optimization and syndication for client-owned properties or products.
3. Research briefs, market maps, and lead qualification using public business data.
4. Content, templates, and operating playbooks sold as digital products.
5. Internal automation services that improve a customer's throughput or cost profile.

## Inbox / Gmail / RAG Constraints
- Only connect to a mailbox when the owner has intentionally provided access.
- Only retrieve messages relevant to a documented workflow such as support triage, CRM cleanup, or proposal extraction.
- Never extract or repurpose personal contacts for unrelated sales activity.
- Store derived outputs in a scoped system of record such as a client CRM, not an open-ended lead dump.

## Financial Safety Gates
- Prefer service revenue and software revenue before any speculative capital deployment.
- If a later phase includes trading or treasury automation, require:
  - paper trading first,
  - explicit position limits,
  - defined stop conditions,
  - separate reserves,
  - and human review before live funds are touched.

## Required Decision Test
Every proposed lane must answer "yes" to all of the following:
1. Is the data source lawful and consent-based?
2. Is the customer value clear without deception?
3. Can the workflow be audited end to end?
4. Can a reasonable operator explain the practice publicly without embarrassment or legal concern?

If any answer is "no", reject or redesign the workflow.
