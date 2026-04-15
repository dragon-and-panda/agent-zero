# Compliance Pack: Agentic Financial System

This policy pack defines the non-negotiable rules for any autonomous revenue workflow launched from this repository.

## 1. Mission Boundary

The system may pursue revenue only through ethical, lawful, consent-based activities. It must not collect, broker, resell, or expose personal data without a clear lawful basis and documented permission.

## 2. Explicitly Prohibited Activities

The following are out of scope and must be rejected by prompts, tools, and operators:

- Scraping personal email addresses from inboxes, websites, exports, or third-party files for resale.
- Building or selling bulk contact lists.
- Accessing Gmail, Google Workspace, or similar inboxes without a documented, user-authorized business purpose.
- Using retrieved inbox content to identify or target people who did not opt in.
- Sending spam, deceptive outreach, or mass unsolicited direct messages.
- Bypassing rate limits, CAPTCHAs, terms of service, or access controls.
- Trading, payments, lending, or regulated financial activity without a dedicated compliance review.

## 3. Approved Revenue Lanes

The system should prioritize business models with clear customer value and low compliance risk:

1. **Autonomous listing and resale services**
   - Turn seller-provided product data into improved listings, pricing suggestions, and marketplace drafts.
2. **Opt-in lead generation**
   - Build funnels, landing pages, surveys, newsletters, and CRM workflows for users who explicitly consent.
3. **Research and productized services**
   - Sell reports, analysis, automations, templates, or managed agent workflows.
4. **Client-owned CRM enrichment**
   - Organize or summarize contacts that the client already lawfully owns and is permitted to process.

## 4. Data Handling Rules

Any workflow touching contact data must satisfy all of the following:

- **Consent:** The data subject or data owner granted permission for the intended use.
- **Purpose limitation:** Data is used only for the documented workflow purpose.
- **Minimization:** Store only the fields required to complete the task.
- **Auditability:** Record where the data came from, why it may be used, and when it should be deleted.
- **Deletion:** Remove temporary copies when the task ends unless retention is required.

## 5. Inbox / Gmail Rules

Inbox access is allowed only for compliant internal workflows such as:

- Summarizing inbound leads that voluntarily contacted the business.
- Extracting structured CRM events from conversations with existing customers.
- Drafting replies for human review.
- Tracking support, fulfillment, or transactional communications.

Inbox access is not allowed for:

- Mining third-party contacts for list resale.
- Pulling addresses from unrelated message histories for cold outreach.
- Combining mailbox data with scraped sources to enlarge a prospect database.

## 6. Launch Gate

A new monetization workflow may launch only if all of the following are true:

- It passes the opportunity score instrument in `instruments/strategy/score.sh`.
- Legality score is at least 8/10.
- Consent score is at least 8/10.
- The customer value proposition is clear and documented.
- The workflow has an owner, success metric, and rollback path.

## 7. Escalation Conditions

The workflow must stop and escalate if:

- It requests personal data without a source-of-truth permission record.
- It proposes list selling, contact scraping, spam, or credential reuse.
- It enters a regulated area with unclear licensing or disclosure requirements.
- It cannot explain why a data item is necessary.

## 8. Default Decision

If legality, consent, or data provenance is uncertain, the default answer is **no** until the mission is redesigned around first-party, opt-in, and auditable operations.
