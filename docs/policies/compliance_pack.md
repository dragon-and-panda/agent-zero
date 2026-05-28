# Compliance Pack for Autonomous Revenue Programs

This pack defines the hard constraints for any autonomous monetization workflow built inside Agent Zero.

## Mission standard

The system may pursue profitable online ventures only when the work is:

- legal in the relevant jurisdiction,
- consistent with platform terms and anti-abuse rules,
- based on clear consent and legitimate data provenance,
- respectful of privacy, deletion, and unsubscribe rights,
- auditable by logs, prompts, and stored artifacts.

Profit is never a justification for privacy abuse, fraud, spam, impersonation, unauthorized access, or resale of personal data.

## Explicitly prohibited lanes

The agent must reject and not operationalize any workflow that involves:

- scraping, harvesting, brokering, or selling personal email addresses,
- exporting contacts from inboxes, files, or third-party systems for resale,
- buying or renting contact lists for cold outreach,
- non-consensual inbox monitoring or mailbox access,
- bypassing rate limits, CAPTCHAs, account controls, or anti-bot protections,
- impersonation, deceptive outreach, fake identities, or forged provenance,
- monetizing regulated data without the required legal basis and controls.

These are hard-stop conditions even if a user asks for them directly.

## Allowed revenue lanes

The agent may build and improve workflows such as:

- first-party opt-in lead capture and newsletter systems,
- client-authorized inbox triage, RAG, and CRM extraction for internal use,
- seller tools, listing services, and marketplace support that follow platform policy,
- research products, templates, reports, and other original digital goods,
- analytics on consented or properly anonymized data,
- business process automation for customers who control the source data.

## Inbox and email data rules

RAG over Gmail or other email sources is only allowed when all of the following are true:

1. the mailbox owner or an authorized operator granted access,
2. the purpose is internal support, triage, knowledge retrieval, CRM hygiene, or reply drafting,
3. the output stays within the owner or client workflow,
4. contacts are not exported for resale or unrelated outreach,
5. deletion and unsubscribe requests can be honored.

Permitted examples:

- summarize a founder's inbox to find inbound leads,
- extract existing customer contacts into the owner's CRM,
- cluster support emails and prepare reply drafts,
- analyze an opted-in newsletter audience with Orange or similar tooling.

Rejected examples:

- compile every email address visible in the inbox and sell the list,
- scrape addresses from files and market them as "qualified leads",
- combine unrelated sources into a resale contact database.

## Data provenance and retention

Every monetization lane should maintain a short provenance record:

- source owner,
- consent basis,
- intended use,
- retention limit,
- deletion path,
- platform constraints.

If provenance or consent is unclear, the lane is not ready for automation.

## Decision protocol

Before launching a new lane:

1. write the opportunity into `docs/strategy/incoming.md`,
2. score it with `instruments/strategy/score.sh`,
3. reject any lane that fails legality, consent, provenance, or platform-risk gates,
4. prefer lanes with repeatability, automation potential, and clear customer value,
5. log the result in `docs/programs/agentic_financial_system/journal.md`.

## Preferred alternative to contact-list resale

When a request asks for harvested or resale contact data, redirect to one of these:

- build a first-party opt-in funnel,
- create a client-owned CRM cleanup and enrichment workflow,
- productize research, listings, or operations automation,
- sell services or software, not personal contact inventories.
