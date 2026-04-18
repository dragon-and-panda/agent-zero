# Compliance Pack for Autonomous Revenue Workflows

This policy pack defines the minimum guardrails for any autonomous workflow that attempts to generate revenue, handle customer data, automate outreach, or publish market-facing content.

## 1. Non-negotiable rules

- Only use lawful, ethical, and consent-based acquisition methods.
- Do not scrape, broker, resell, or distribute personal email addresses or contact lists.
- Do not access private inboxes, messages, or accounts without explicit authorization from the account owner.
- Do not send spam, deceptive outreach, or messages that violate platform terms.
- Do not bypass CAPTCHAs, rate limits, authentication controls, or anti-abuse protections.
- Do not make legal, tax, medical, investment, or compliance claims without a cited basis and an explicit review path.

## 2. Prohibited monetization patterns

The following are out of scope and must be rejected:

- Building or selling personal email databases.
- Harvesting contacts from Gmail, Google Workspace, scraped pages, leaked files, or third-party datasets without verified consent.
- Mass cold outreach campaigns using unclear data provenance.
- Marketplace or messaging automation that violates a platform's terms of service.
- Any workflow whose primary value depends on privacy invasion, impersonation, fraud, or evasion.

## 3. Approved revenue lanes

Autonomous workflows may proceed when they fit one of these patterns:

1. First-party inbox to CRM automation
   - Operates only on an inbox owned or explicitly authorized by the customer.
   - Extracts leads from inbound messages or existing opt-in relationships.
   - Stores provenance, consent state, and unsubscribe status.

2. Opt-in audience products
   - Newsletters, research subscriptions, watchlists, or benchmarking products.
   - Subscribers join voluntarily and can leave easily.

3. Listing and commerce automation
   - Product listing generation, inventory operations, response drafting, and post-sale workflows.
   - Must follow each platform's content and automation rules.

4. Client service automation
   - Proposal generation, intake triage, CRM enrichment from client-owned systems, reporting, and onboarding.
   - Customer data must stay within the customer's lawful control boundary.

## 4. Required pre-launch checks

Every autonomous revenue idea must document:

- Target customer and value proposition.
- Data provenance.
- Consent model.
- Platform or channel terms review.
- Pricing, margin, and fulfillment model.
- Fallback manual path if automation is blocked.

If any of the following are weak or unknown, the workflow is held or rejected:

- legality
- consent
- provenance
- platform terms compatibility

## 5. Enforcement checklist

Before enabling a workflow, confirm:

- The data source is first-party, opt-in, public-domain, or contractually licensed.
- The customer can explain why they are allowed to use the data.
- The workflow exposes unsubscribe, deletion, and audit paths when applicable.
- Critical decisions are logged in the mission diary and strategy queue.
- Risky steps have a human-review fallback.

## 6. Escalation rules

Escalate and pause the workflow if:

- a request asks for inbox scraping or contact resale
- a workflow depends on unclear consent
- the platform terms appear to prohibit the planned automation
- regulated claims or financial promises are introduced

When escalation happens, replace the request with a compliant alternative such as:

- opt-in lead capture
- customer-owned inbox triage
- listing automation
- research products
- agency services built on consented customer systems
