# Compliance Pack for Autonomous Revenue Programs

This pack governs any Agent Zero workflow that touches monetization, outreach, inbox data, customer data, or platform automation.

## 1. Non-Negotiable Rules

- Do not scrape, harvest, broker, resell, or package personal email addresses or contact lists.
- Do not access, analyze, or export mailbox data unless the mailbox is owned by the operator or explicit written authorization exists.
- Do not use Gmail, IMAP, exported inboxes, or third-party datasets to assemble prospect lists for sale.
- Do not send spam, cold outreach at scale without a lawful basis, or messages that violate anti-spam rules or platform terms.
- Do not bypass CAPTCHAs, rate limits, authentication, or anti-bot controls.
- Do not misrepresent identity, affiliation, intent, or product capabilities.
- Do not run regulated financial activities, lending, broker-dealer behavior, or investment solicitation without the required licensing and controls.

## 2. Allowed Revenue Lanes

Allowed lanes must rely on first-party, consented, or lawfully licensed data and must stay within the target platform's rules.

Examples:

- Opt-in lead magnets and newsletter funnels
- Client-owned inbox triage that routes inbound leads into a CRM
- Productized services built from user-provided assets
- Digital products, templates, reports, and research subscriptions
- Marketplace listing automation that operates on the seller's own inventory
- Affiliate or partner programs that permit the promotion method being used

## 3. Gmail and Email Data Policy

RAG over email is only allowed when all of the following are true:

1. The mailbox belongs to the operator or a client that has explicitly authorized access.
2. The purpose is internal productivity, support, CRM hygiene, or customer service.
3. Retrieved content is minimized to the task and not repackaged as a salable contact dataset.
4. Storage, retention, and downstream use follow the mailbox owner's policy and applicable law.

Disallowed examples:

- "Compile every email address in the inbox and sell the list."
- "Export senders from Gmail and upload them to a lead marketplace."
- "Scrape signatures, merge them with web searches, and build a resale database."

Allowed examples:

- "Classify inbound sales emails in a client-owned inbox and draft replies."
- "Summarize support conversations to improve help-center content."
- "Extract company names from authorized inbox threads to update the client's CRM."

## 4. Activation Gates for New Ventures

Every venture lane must clear all four hard gates before activation:

1. Legality: the workflow is lawful in the relevant jurisdiction.
2. Consent: the data subject or data owner has opted in or authorized the use.
3. Provenance: the data source is first-party, client-owned, or properly licensed.
4. Terms: the workflow complies with the platform, API, and marketplace rules in play.

If any hard gate fails, the lane is rejected.

## 5. Operating Pattern

Each monetization idea should be processed as:

1. Screen with the `revenue_planning` tool.
2. Score with `instruments/strategy/score.sh`.
3. Record the lane in `docs/strategy/incoming.md`.
4. If accepted, execute through the program charter and journal under `docs/programs/agentic_financial_system/`.

## 6. Preferred Phase 1 Revenue Focus

Prefer early lanes with:

- fast delivery using existing repo capabilities
- low compliance overhead
- strong margins
- repeatable fulfillment
- clear customer ownership of the source data

Current preferred starting points:

- client-owned inbox-to-CRM automation
- autonomous listing and resale services for seller-owned inventory
- research, templates, and niche information products

## 7. Escalation Triggers

Pause and escalate the lane if any of the following appears:

- requests to sell contact lists or personal data
- unclear consent or unclear data ownership
- unclear licensing of source data
- scraping or automation that appears to violate terms
- regulated financial claims, guarantees, or fiduciary behavior

When escalated, convert the request into a compliant alternative rather than trying to partially fulfill the unsafe version.
