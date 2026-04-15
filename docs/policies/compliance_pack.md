# Compliance Pack for Autonomous Revenue Workflows

This pack defines the minimum legal, privacy, and ethics rules for any revenue-oriented workflow run inside this repository.

## 1. Hard Prohibitions

The system must not:

- scrape, export, broker, or sell personal email addresses or contact lists without explicit, documented consent from the data subjects or the data owner with a lawful basis for processing;
- access Gmail, Google Workspace, inboxes, CRMs, or cloud files without the account owner's informed authorization;
- use inbox-derived data to create resale lists, spam campaigns, or undisclosed profiling datasets;
- send bulk outreach that violates CAN-SPAM, GDPR, ePrivacy, CASL, platform terms, or local anti-spam/privacy laws;
- misrepresent identity, fabricate testimonials, impersonate buyers, or conceal automated activity where disclosure is required;
- bypass rate limits, captchas, access controls, or terms of service to obtain leads or market data.

Requests that depend on any prohibited workflow must be rejected or reframed into a compliant alternative.

## 2. Approved Data Access Pattern

Gmail or Google email data may only be used when all of the following are true:

1. the mailbox owner has explicitly authorized the access;
2. the purpose is internal productivity, analytics, CRM hygiene, support triage, or another legitimate first-party use;
3. the workflow collects only the minimum data needed;
4. retention, deletion, and audit logging are defined up front;
5. the output is not sold as a personal data asset.

Approved examples:

- inbox-to-CRM cleanup for a client that owns the mailbox;
- support-ticket summarization from a shared operations inbox;
- RAG over the user's own historical email for search, SOP extraction, or task follow-up.

Disallowed examples:

- mining contacts from email archives to build a marketable lead list;
- combining scraped contacts with inbox contacts for outbound spam;
- reselling any list created from mailbox, CRM, or support data.

## 3. Approved Monetization Lanes

Prefer revenue sources that are lawful, consent-based, and durable:

- first-party SaaS or service products;
- consent-based lead capture systems and CRM enrichment for the client that owns the audience;
- listing optimization, content operations, research products, analytics dashboards, and workflow automation;
- affiliate or partner revenue with transparent disclosure;
- subscription intelligence products built from public, licensed, or customer-owned data.

## 4. Pre-Launch Compliance Checklist

Before any workflow moves from idea to execution, verify:

- lawful data source;
- documented consent or contract authority where needed;
- terms-of-service compatibility;
- minimum-data collection;
- retention/deletion plan;
- disclosure requirements for automation and affiliate activity;
- fallback path if legal basis, consent, or platform rules are uncertain.

If any item fails, the workflow remains on HOLD or is marked REJECT.

## 5. Response Policy for Unsafe Revenue Requests

When asked to monetize through harvested emails, scraped personal data, or mailbox-derived list sales, the system should:

1. clearly decline the unsafe action;
2. explain the legal/privacy problem in one sentence;
3. redirect to a compliant substitute, such as:
   - opt-in lead magnet funnel,
   - client-owned inbox intelligence,
   - public-data market research,
   - productized service or subscription workflow.

## 6. Audit Expectations

Each approved revenue lane should maintain:

- a written charter,
- a scoring record,
- a journal of decisions and evidence,
- a list of blocked or rejected ideas.

These artifacts should live under `docs/programs/` and `docs/strategy/`.
