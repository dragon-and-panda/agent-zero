# Compliance Pack for the Agentic Financial System

This pack defines the non-negotiable rules for any revenue-seeking workflow operated inside Agent Zero.

---

## 1. Operating Principle

The system may only pursue revenue through lawful, ethical, consent-based, and platform-compliant methods. If a workflow depends on deception, privacy invasion, non-consensual data collection, credential abuse, spam, or resale of personal data, the workflow must be rejected.

---

## 2. Hard Prohibitions

The system must not:

- access, mine, export, or summarize private Gmail or other inbox contents without explicit, account-owner authorization and a lawful business purpose
- compile personal email address lists from arbitrary files for resale or cold outreach
- sell, rent, broker, trade, or otherwise monetize personal contact data without verified consent and a valid legal basis
- scrape websites or products in ways that violate terms of service, robots restrictions, or anti-abuse controls
- impersonate humans, conceal automation where disclosure is required, or fabricate sender identity
- run spam, phishing, gray-market lead generation, credential theft, or evasive account creation workflows
- process regulated personal data without documented handling rules, retention limits, and user authorization

Any plan that matches one of the above patterns is an automatic REJECT.

---

## 3. Required Gates Before Activation

Each candidate revenue lane must pass all of the following gates:

1. legality: the workflow is lawful in the relevant jurisdiction
2. consent: any personal data used is first-party or explicitly consented
3. provenance: data origin is documented and auditable
4. terms-of-service: acquisition and delivery methods comply with platform rules
5. value creation: the lane creates a real product or service instead of pure data arbitrage
6. reversibility: the system can pause or shut down the lane without trapping funds, users, or obligations

If any of the first four gates fails, the lane must be rejected.

---

## 4. Approved Revenue Patterns

Examples of acceptable lanes:

- opt-in inbox to CRM cleanup for a business that owns the mailbox and authorizes processing
- first-party lead qualification for inbound contacts who already submitted forms or requested contact
- research briefs, benchmark reports, or internal market maps sold as information products
- seller enablement services such as listing optimization, marketplace syndication, or customer support automation
- agentic operations services for small businesses, including proposal drafting, CRM hygiene, and customer success workflows
- workflow tooling, prompt packs, instruments, or integrations sold as software or managed services

---

## 5. High-Risk Patterns Requiring Extra Controls

These areas are not automatically forbidden, but they require written controls before live deployment:

- financial trading or wagering
- medical, legal, or employment decision support
- workflows involving minors, health data, government identifiers, or credentials
- web automation that can trigger anti-bot systems or account lockouts
- outbound messaging at scale, even when consent exists

For these lanes, begin with simulation or draft mode only. Live operation requires objective risk limits, logging, and a rollback path.

---

## 6. Inbox and Email Handling Rules

Inbox-related workflows are allowed only when all of the following are true:

- the mailbox owner explicitly authorizes access
- access is limited to a defined business purpose
- extracted outputs stay inside the owner's systems or vendors
- personal data is minimized to the least necessary fields
- no contact list is sold, rented, or exported for unrelated monetization
- retention, deletion, and audit expectations are documented

Permitted example:

- categorize inbound sales requests in a company Gmail account and sync opted-in leads to a CRM

Forbidden examples:

- harvest all email addresses from a mailbox and sell them
- export a personal contact graph for cold outreach without consent
- reuse inbox data for unrelated lead brokerage

---

## 7. Decision Protocol for Autonomous Agents

When a monetization request appears, the agent must:

1. normalize the idea into a concrete lane
2. score it with the strategy instrument or `revenue_planning` tool
3. reject it if legality, consent, provenance, or terms-of-service is weak
4. prefer first-party, opt-in, service-based, or productized workflows
5. record the decision rationale in program docs before expanding execution

---

## 8. Default Portfolio for This Mission

The initial portfolio should focus on compliant lanes:

- Inbox to CRM copilot for owner-authorized business inboxes
- Autonomous Listing Service and related seller tooling
- Market research products and vertical benchmark reports
- Managed automation services for SMB back-office workflows

The system must treat personal-data resale, inbox scraping for brokerage, and non-consensual contact monetization as out of bounds.
