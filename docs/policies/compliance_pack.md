# Compliance Pack: Agentic Financial System

This policy pack defines the minimum legal, ethical, and platform-compliance requirements for any autonomous revenue program operated with Agent Zero.

It exists to keep the program aligned with lawful, consent-based commercialization. Revenue is not a justification for privacy abuse, deceptive outreach, or prohibited data brokerage.

---

## 1. Non-Negotiable Rules

The system must not:

- scrape, compile, broker, rent, or sell personal email addresses or contact lists
- use Gmail, Google Workspace, or any inbox data to extract third-party contacts without clear authorization and a legitimate business purpose
- send spam, cold outreach at scale without consent where consent is required, or evade unsubscribe requirements
- bypass platform terms of service, anti-bot protections, rate limits, or account controls
- misrepresent identity, fabricate endorsements, or impersonate humans during sales or outreach
- process regulated, sensitive, or confidential data outside the scope of the user's clear authorization

Any lane that depends on personal-data resale, non-consensual inbox mining, or deceptive acquisition is out of scope and must be rejected.

---

## 2. Allowed Data Sources

Approved data use is limited to one or more of the following:

- first-party data collected directly from the operator's own customers or prospects with proper notice
- client-owned data where the client has the legal right to authorize processing
- public business information that is permitted by source terms and applicable law
- opt-in subscriber data collected through clear forms, lead magnets, waitlists, or purchases
- synthetic, demo, or sandbox datasets used for testing and evaluation

If provenance is unclear, the opportunity remains blocked until provenance is documented.

---

## 3. Inbox and Email Handling Rules

Inbox-connected workflows are only allowed for:

- triaging inbound messages for the account owner
- extracting first-party customer intents, FAQs, and support signals
- syncing customer-approved records into a CRM or task system
- producing summaries, labels, and suggested replies for the authorized mailbox owner

Inbox-connected workflows are not allowed for:

- harvesting third-party contact lists from historical threads
- building prospect databases from correspondence not originally collected for that purpose
- exporting or packaging contacts for sale to outside buyers

Any Gmail or Google email RAG workflow must be scoped to customer support, operations, sales-assist on owned relationships, or knowledge retrieval for the mailbox owner.

---

## 4. Revenue Lanes That Are In Scope

The following lane types are acceptable if all other guardrails pass:

1. **Opt-in lead generation**
   - Landing pages, lead magnets, newsletters, and waitlists.
   - Double opt-in preferred where feasible.

2. **Client-owned workflow automation**
   - Inbox triage, CRM updates, proposal generation, quoting, support operations, and internal knowledge retrieval.

3. **Autonomous listing and commerce services**
   - Services that improve product listings, merchandising, customer response times, and marketplace operations.

4. **Research and intelligence products**
   - Market maps, compliance summaries, pricing intelligence, monitoring dashboards, or internal reports delivered to paying clients.

5. **Software or agent services**
   - Retainers or subscriptions for lawful automation, analytics, and operating systems that reduce manual work.

---

## 5. Gating Checklist Before Activation

Every new lane must clear all of the following:

- **Legality:** The business model is lawful in the target jurisdiction.
- **Consent:** Any personal data use is tied to valid authorization or opt-in.
- **Provenance:** Data sources are documented and traceable.
- **Terms of service:** The workflow does not require prohibited automation or scraping.
- **Operational safety:** The system has rate limits, logging, and a rollback path.
- **Brand integrity:** The workflow is honest about who is communicating and why.

If any hard gate fails, the lane is rejected and cannot move to build or launch.

---

## 6. Required Operating Controls

Each production lane must maintain:

- a written charter in `docs/programs/`
- a mission journal capturing decisions, tests, and outcomes
- a scoring record using `instruments/strategy/score.sh`
- basic telemetry for revenue, conversion, cost, and failure rate
- a manual stop condition for compliance incidents or customer complaints

---

## 7. Rejected Example

**Idea:** Use RAG over Google email data to compile email address lists and sell those lists to online services.

**Decision:** Reject.

**Reason:** The lane depends on personal data extraction, unclear consent, poor provenance for downstream reuse, and likely platform, privacy, and anti-spam violations. It fails the legality, consent, and provenance gates.

---

## 8. Preferred Replacement

Replace contact-list resale with one or more of:

- opt-in audience building
- client-authorized inbox-to-CRM systems
- listing automation services
- market research subscriptions
- agent implementation retainers for small businesses

These lanes can still be highly automatable and profitable without relying on unlawful or unethical data acquisition.
