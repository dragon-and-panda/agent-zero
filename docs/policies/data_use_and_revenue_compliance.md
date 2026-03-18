# Data Use and Revenue Compliance Policy

This policy governs any revenue-oriented workflow built on top of Agent Zero in this repository.

---

## 1. Purpose

Protect individuals, the operator, and the business by ensuring revenue workflows use personal data lawfully, ethically, and minimally.

---

## 2. Default Rule

Personal data may be processed only when there is a clear, documented basis for the exact use case.

If the basis is unclear, the workflow must:

- reduce scope,
- store less data,
- avoid outbound action,
- or stop entirely.

---

## 3. Prohibited Actions

The following are not allowed:

- selling or brokering email addresses extracted from inboxes, sent mail, CC fields, files, or contact exports;
- scraping personal contact data from websites, social platforms, or third-party tools without permission;
- importing contacts into marketing systems without opt-in or another clearly documented authorization;
- disguising cold outreach as transactional or support messaging;
- using mailbox data to enrich third-party lead databases;
- automating platform abuse, spam, or evasion of rate limits and anti-bot controls;
- routing operating revenue directly to a personal payment handle as a substitute for normal business bookkeeping.

---

## 4. Allowed Data Uses

The following uses are allowed when the mailbox owner or customer has authorized access:

- internal search and retrieval,
- customer support context,
- invoice, quote, or project follow-up,
- CRM deduplication and hygiene,
- relationship mapping,
- explicit newsletter or waitlist management,
- one-to-one follow-up with known contacts where the message is relevant and permitted.

---

## 5. Consent and Contact Statuses

Every extracted contact should be assigned one status:

- `opted_in`
- `transactional_only`
- `contractual`
- `internal`
- `unknown`
- `do_not_contact`

Rules:

- `opted_in`: may receive the consented communication type.
- `transactional_only`: only account, support, billing, or service-delivery messages.
- `contractual`: only messages tied to the active commercial relationship.
- `internal`: internal coordination only.
- `unknown`: no marketing or bulk outreach.
- `do_not_contact`: no outbound communication except legally required notices.

---

## 6. Data Minimization

Store only the fields required for the approved workflow, such as:

- email address,
- display name,
- source,
- last interaction date,
- consent status,
- relationship type,
- limited notes.

Do not store full mailbox contents in downstream tools unless necessary for the task and covered by authorization.

---

## 7. Security and Retention

- Restrict access to mailbox-derived data to the minimum set of workflows and operators.
- Prefer derived summaries over raw message bodies.
- Delete stale or unauthorized contact records.
- Keep an audit trail of where a contact came from and why it is retained.

---

## 8. Revenue Operations Rules

- Revenue should enter a business-controlled account with normal accounting records.
- Owner distributions should be handled through standard bookkeeping, not ad hoc transfer automation.
- New monetization experiments must be scored for compliance, setup cost, and downside before launch.
- Speculative trading must not begin until operating reserves and paper-trading validation are documented.

---

## 9. Escalation Triggers

Pause the workflow and require review if any of the following occur:

- unclear consent or source provenance,
- requests to sell or share contact databases,
- high-volume outreach to unknown recipients,
- legal threats, complaints, or unsubscribe violations,
- platform warnings for abuse or spam,
- proposals to use real capital in leveraged trading.

---

## 10. Enforcement

If a workflow conflicts with this policy, the policy wins. The workflow must be redesigned toward first-party data, explicit consent, and durable value creation.
