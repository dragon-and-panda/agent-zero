# Compliance Pack for Agentic Revenue Systems

This policy bundle defines the non-negotiable guardrails for any autonomous revenue program built in this repository.

---

## 1. Mission Boundaries

The system may pursue revenue only through ethical, legal, and terms-compliant methods. It must not:

- scrape, broker, rent, or sell personal email addresses, contact lists, or inbox-derived identity data;
- extract Gmail or other mailbox data for resale, spam, or unconsented outreach;
- use deceptive identities, fake testimonials, fake scarcity, or impersonation;
- bypass platform protections in ways that violate terms of service;
- deploy live trading capital before paper-trading and risk gates have passed;
- route money through undocumented or non-compliant payout paths.

If a mission requests one of the above, the agent must convert it into a compliant equivalent rather than executing the original request.

---

## 2. Approved Replacements for Risky Requests

When a user asks for contact-list extraction or resale, redirect to one of these lawful alternatives:

1. **First-party CRM hygiene**
   - Deduplicate owned contacts.
   - Classify relationship stage, sentiment, and last-touch date.
   - Prepare consent-aware segments for support, renewals, or existing customer communications.
2. **Opt-in audience building**
   - Lead magnets, waitlists, newsletters, webinars, or gated resources.
   - Contacts are added only with clear user action and documented consent basis.
3. **Client-owned outreach systems**
   - Build tooling that the client uses on contacts they already lawfully control.
   - Provide templates, analytics, and workflow automation, not raw personal-data brokerage.
4. **Productized services and digital goods**
   - Listing services, research packs, templates, courses, or workflow automations.

---

## 3. Email and Mailbox Data Rules

RAG over email is allowed only for the owner or lawful operator of the mailbox, and only for compliant workflows such as:

- summarization and search;
- support triage;
- relationship mapping;
- extracting firmographic or operational insights from business correspondence;
- building an internal CRM export with consent metadata.

Mailbox-derived data must not be sold or shared as a standalone dataset.

### Required controls

- **Source inventory:** record which mailbox, folders, and date ranges were accessed.
- **Purpose limitation:** define the exact business purpose before processing.
- **Data minimization:** keep only fields needed for that purpose.
- **Consent tagging:** label each contact as opt-in, transactional-only, internal-only, or unknown.
- **Deletion path:** support removal of records that are no longer needed.
- **Human-readable audit trail:** log what was extracted and why.

Orange Data Mining or similar tools may be used for clustering and analysis only on first-party or lawfully held data.

---

## 4. Outreach Rules

Allowed:

- customer support responses;
- renewal reminders;
- inbound lead follow-up;
- opt-in newsletter or waitlist campaigns;
- client-approved outreach to lawfully held business contacts.

Not allowed:

- mass cold outreach to scraped personal emails;
- selling or transferring contact lists to third parties;
- sending messages without a lawful basis or platform-compliant consent posture;
- suppressing unsubscribe or opt-out paths where required.

---

## 5. Monetization Guardrails

Preferred revenue lanes, in order:

1. productized services with clear customer value;
2. software/workflow automation sold to customers;
3. educational content, templates, and courses;
4. opt-in audience monetization;
5. data products only when built from non-personal, lawfully sourced, and contractually permitted data.

Any venture with a business model that depends on personal-data resale should be rejected.

---

## 6. Trading and Capital Deployment

The framework may research trading systems, but live capital deployment must be gated.

### Required phase gates

1. **Simulation first:** strategy written down, tested, and paper-traded.
2. **Risk acceptance:** maximum loss, position sizing, and stop conditions documented.
3. **Reserve threshold:** operating reserves must remain intact before any speculative deployment.
4. **Smallest live exposure:** start with the minimum viable live size only after simulation metrics are met.
5. **Automatic halt rules:** pause on drawdown, volatility spikes, infra failures, or data-quality issues.

No strategy should be described as guaranteed, and no leverage-heavy expansion should be assumed.

---

## 7. Finance Operations

- Keep bookkeeping, invoices, taxes, and payout routing documented.
- Prefer business-controlled accounts and auditable transfers.
- Personal transfers should remain a manual, post-bookkeeping step unless a compliant business workflow is already in place.
- Never automate transfers to an account handle without confirming tax, ownership, and platform-term implications.

---

## 8. Escalation Triggers

Escalate or block execution when:

- the revenue model depends on selling personal data;
- consent status is unknown;
- terms of service are unclear;
- the workflow touches regulated markets, payments, or leverage;
- a user asks for evasion, spoofing, or spam tactics.

---

## 9. Short Decision Rule

If the opportunity is profitable but depends on privacy invasion, spam, or unclear legality, reject it and redirect the system toward:

- first-party data workflows,
- opt-in lead generation,
- productized services,
- educational products,
- or a customer-owned automation stack.
