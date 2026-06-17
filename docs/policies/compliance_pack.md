# Compliance Pack for Autonomous Revenue Missions

This policy pack governs any Agent Zero workflow aimed at generating revenue with minimal human supervision.

---

## 1. Core Rules

1. **Legal first:** Do not start or continue a revenue workflow that appears unlawful in the target jurisdiction.
2. **Consent first:** Do not ingest, analyze, or act on personal communications or contact records without explicit authorization from the data owner.
3. **No spam operations:** Do not build workflows for scraping, brokering, renting, or selling personal email lists or other personal contact databases.
4. **No deceptive acquisition:** Do not impersonate humans, hide commercial intent, or bypass platform rules, anti-bot protections, or privacy controls.
5. **Minimum necessary data:** Use only the data needed to deliver the service and avoid storing raw sensitive content when structured summaries will do.
6. **Auditability:** Every autonomous mission should leave an artifact trail covering inputs, decisions, outputs, and stop conditions.

---

## 2. Approved Revenue Patterns

These are acceptable patterns for this repo's autonomous financial system:

- **Consent-based Inbox-to-CRM Hygiene Service**
  - Analyze a user's own Gmail or Workspace mailbox.
  - Extract leads, follow-ups, support requests, and CRM tasks for that same user or organization.
  - Summarize inbox data with RAG for internal productivity or customer service operations.
- **Autonomous Listing / Concierge Services**
  - Produce listings, pricing suggestions, and client-facing sales materials for products the client already owns and is authorized to sell.
- **Research Products**
  - Generate market maps, competitor reports, public-data dashboards, and opt-in newsletters from public, licensed, or first-party sources.
- **Templates / Advisory / Automation Services**
  - Sell prompts, playbooks, dashboards, automations, and operational services that improve clients' lawful workflows.

---

## 3. Prohibited Patterns

The following are out of scope and must be rejected:

- Compiling or selling personal email lists.
- Scraping inboxes, websites, or files for contact data that will be resold or used for unsolicited outreach.
- Accessing Gmail, Workspace, or other mailboxes without clear authorization from the mailbox owner.
- Generating outreach intended to evade spam rules or consent requirements.
- Mass-importing arbitrary "relevant files" for contact extraction when ownership, consent, or purpose is unclear.

---

## 4. Gmail / Email RAG Guardrails

RAG over email content is only allowed when all of the following are true:

1. The mailbox belongs to the user or to an organization that has explicitly authorized the workflow.
2. The purpose is internal productivity, support triage, CRM hygiene, sales operations for existing lawful relationships, or similar first-party use.
3. Output is restricted to summaries, tasks, labels, client-owned contact records, or analytics that remain under the client's control.
4. The system does not package or resell extracted personal data to third parties.
5. Access and retention are documented, revocable, and minimized.

Recommended safe outputs:

- Follow-up queue
- Reply drafts for the mailbox owner
- Contact deduplication within the client's own CRM
- Opportunity tagging
- Support / sales trend analysis

---

## 5. Decision Gate

Before activating a new money-making lane, score it across:

- legality
- consent posture
- time to cash
- repeatability
- defensibility
- setup ease

Any lane that fails legality or consent should be marked **REJECT** regardless of apparent upside.

Use `instruments/strategy/score.sh` for the first-pass decision.

---

## 6. Escalation Rules

Escalate or halt the workflow when:

- the data source includes personal communications without explicit ownership/authorization,
- a platform's terms or community rules prohibit the planned automation,
- a revenue idea depends on resale of personal data,
- compliance status cannot be verified from the available evidence.

Default action when uncertain: **HOLD** or **REJECT**, not **GO**.
