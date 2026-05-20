# Compliance Pack for Autonomous Revenue Work

This pack defines the minimum rules for any Agent Zero workflow that touches monetization, customer acquisition, inbox data, or third-party platforms.

## 1. Non-negotiable prohibitions

The system must not:

- harvest personal email addresses from Gmail, local files, websites, or scraped datasets for resale or cold-list building
- compile, broker, rent, or sell contact lists or other personal data
- send spam or automate outreach without a lawful basis, clear authorization, and an unsubscribe path where required
- use inbox access that is not explicitly owned or authorized by the account holder
- bypass platform restrictions, anti-bot systems, CAPTCHAs, account limits, or terms of service
- misrepresent identity, consent status, or how contact data was obtained

Any lane that depends on one of the above is an automatic REJECT.

## 2. Allowed mailbox and RAG use

Mailbox retrieval and RAG are allowed only when all of the following are true:

1. The mailbox belongs to the user or the user has explicit authority to automate it.
2. The workflow is tied to a legitimate business purpose such as support triage, invoice extraction, customer follow-up, CRM synchronization, or knowledge retrieval for ongoing customer relationships.
3. The system uses the minimum necessary data and does not bulk-export contacts for resale, enrichment, or spam.
4. Retention, deletion, and access controls are documented.

Examples of allowed mailbox workflows:

- summarize inbound customer requests
- extract invoices, receipts, and purchase orders
- tag opted-in leads and sync them into a CRM
- retrieve prior conversation context before replying to an existing customer

## 3. Approved monetization patterns

Prefer revenue lanes that are first-party, consent-based, and operationally defensible:

- opt-in newsletters, lead magnets, and owned audience products
- client-authorized inbox-to-CRM and customer-operations automation
- AI-enabled listing, resale, and marketplace services that follow platform rules
- research, analytics, and benchmarking products built from public or licensed data
- workflow automation sold as a service to clients who control their own data and channels

## 4. Hard gates before activation

Every monetization lane must be screened on four hard gates:

- legality
- consent
- data provenance
- platform risk

Use `instruments/strategy/score.sh` or the `revenue_planning` tool before enabling a lane.

Gate outcomes:

- low legality, low consent, or low provenance -> REJECT
- high platform risk -> REJECT
- medium on any hard gate -> HOLD until clarified

## 5. Execution checklist

Before launching a lane, record:

1. customer and value proposition
2. acquisition channel and why it is lawful
3. data sources and why they are authorized
4. platform dependencies and mitigation plan
5. pricing, margin, and repeatability assumptions
6. audit trail location in `docs/programs/agentic_financial_system/`

## 6. Safe replacements for rejected ideas

If a plan fails because it relies on harvested contacts or inbox mining, replace it with one of these:

- first-party signup funnels
- referral programs
- partnerships with audience owners
- content, SEO, or marketplace discovery
- client-owned CRM automation
- public-data research products

## 7. Operating rule

When a mission includes both safe and unsafe components, execute only the safe subset and rewrite the rest into a compliant equivalent.
