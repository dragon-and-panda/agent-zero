# Compliance Pack for the Agentic Financial System

This pack defines the minimum safety, privacy, and platform-compliance rules for any revenue-seeking workflow built with Agent Zero.

## 1. Mission Boundary

The system may pursue autonomous revenue only through lawful, ethical, consent-based products and services. Revenue is not a justification for privacy invasion, spam, data brokerage, impersonation, or platform abuse.

## 2. Explicitly Prohibited Workflows

Do not build, automate, or monetize any workflow that relies on:

- scraping or reselling personal email addresses, inbox contents, or contact lists
- selling, brokering, renting, or trading personal data gathered from files, Gmail, or other private systems
- accessing mailboxes, drives, or accounts without explicit owner authorization
- mass unsolicited outreach that lacks a defensible consent basis
- evading platform rules, rate limits, CAPTCHA controls, or anti-abuse systems
- deceptive identity claims, fake personas, fabricated testimonials, or undisclosed automation where disclosure is required
- harvesting credentials, tokens, or regulated data for resale or lead generation

Unsafe examples to reject immediately:

- "Compile email lists from Gmail and sell them"
- "Extract contact lists from files and broker them"
- "Use inbox data to build a marketing database for third parties"

## 3. Allowed Revenue Patterns

Prioritize revenue lanes with strong consent, clear delivery, and durable customer value:

- first-party, opt-in newsletters and communities
- client-owned CRM cleanup, deduplication, and reply drafting under contract
- inbox triage or RAG assistants for the mailbox owner
- research products, market maps, or workflow audits built from lawful sources
- listing optimization, marketplace operations, and other service businesses
- agentic automation that saves time or improves conversion for paying customers without reselling their data

## 4. Gmail and RAG Rules

Gmail or email-derived data may only be used when all of the following are true:

1. the mailbox owner or authorized business explicitly approved the access
2. the purpose is owner benefit, not third-party list resale
3. the data flow is minimized to the smallest useful scope
4. sensitive data is redacted or excluded from long-lived stores when possible
5. any exported knowledge base preserves provenance and retention limits

Approved examples:

- summarizing a founder's inbox into follow-up tasks
- building a reply assistant for a support mailbox owned by the customer
- extracting customer support themes for the mailbox owner's internal reporting

Disallowed examples:

- mining recipient addresses to create a lead list for resale
- turning email threads into a prospect database for unrelated outreach

## 5. Data Provenance Rules

Every monetization idea must classify its inputs before activation:

- `first-party`: directly collected from the operator's own audience with notice and consent
- `client-owned`: provided by a customer under contract and used only for that customer
- `public-nonpersonal`: lawful public data that does not create a personal-data resale workflow
- `unclear`: provenance cannot be demonstrated
- `prohibited`: scraped private data, brokered personal data, or non-consensual contact data

Anything marked `unclear` or `prohibited` fails the activation gate.

## 6. Platform and Outreach Rules

- Respect product terms of service, robots restrictions, API terms, and marketplace posting limits.
- Prefer inbound demand, opt-in funnels, and permission-based outreach over cold automation.
- If outreach is allowed, keep lists first-party or client-owned and maintain suppression and consent records.
- Do not treat "it is technically possible" as evidence that a workflow is allowed.

## 7. Orange / Data Analysis Rule

Orange or any other analysis tool may be used only on datasets that are owner-controlled, contractually supplied, synthetic, or otherwise compliant with the provenance rules above. Analysis tools do not make an unlawful dataset lawful.

## 8. Activation Gate

Before any lane goes live, it must pass all hard gates:

- legality
- consent
- data provenance
- platform terms compliance
- delivery feasibility

Use `python/tools/revenue_planning.py` and `instruments/strategy/score.sh` to record that decision. Any failed hard gate means reject or redesign the lane.

## 9. Preferred Phase 1 Revenue Lanes

Phase 1 should focus on low-complexity, consent-based offers:

1. inbox-to-CRM assistant for owner-controlled mailboxes
2. autonomous listing and resale operations
3. research briefs and market intelligence products
4. client automation audits and implementation retainers

## 10. Escalation Rule

If a proposed workflow touches private communications, personal data resale, regulated records, or ambiguous consent, stop and redesign the plan around first-party or client-owned data with explicit authorization.
