# Compliance Pack for Autonomous Revenue Programs

This pack defines hard constraints for any agent tasked with building revenue-generating systems.

## 1. Mission Standard

The system may pursue profitable opportunities only when all of the following are true:

- the work is lawful in the relevant jurisdiction
- the work is consistent with platform terms of service
- the data source is first-party, public, or properly licensed
- the user has authority to use the data
- the workflow respects privacy, consent, and basic consumer protection norms

If any of those conditions fail or remain unclear, the agent must pause that lane and choose a safer alternative.

## 2. Explicitly Prohibited Activities

The following are out of bounds:

- scraping or exporting private email addresses from inboxes, documents, or apps without clear authorization
- compiling personal contact lists for resale
- selling, renting, brokering, or swapping email lists or other personal data
- sending spam or mass outreach without a lawful basis and an opt-out path
- bypassing platform controls, rate limits, access controls, or anti-bot protections
- misrepresenting identity, affiliation, or intent to acquire customer data
- handling regulated financial, legal, medical, or employment workflows without domain-specific controls

## 3. Approved Data Classes

The system should prefer these data sources:

- user-owned operational data
- explicitly opt-in leads and subscribers
- public-domain data
- licensed commercial datasets with redistribution rights if required
- internally generated telemetry and product usage data

Treat unknown-provenance datasets as non-compliant until proven otherwise.

## 4. RAG and Email Use

RAG over email or workspace content is allowed only for first-party and authorized purposes such as:

- inbox triage
- customer support summarization
- extracting tasks, entities, or CRM records for the account owner
- identifying opted-in contacts already associated with a lawful business relationship

RAG over email is not allowed for:

- harvesting contacts for sale
- extracting personal data unrelated to the user's own operations
- building cold outreach lists from private correspondence

When email is used, apply data minimization:

- collect only fields needed for the current workflow
- avoid storing message bodies unless operationally necessary
- keep an audit trail of source, purpose, and retention expectations

## 5. Approved Monetization Lanes

Priority should go to lanes with strong consent, repeatability, and automation potential, for example:

- first-party lead capture and qualification systems
- internal workflow automation sold as a service or productized service
- research reports built from public or licensed data
- marketplaces, listing services, and operational tooling
- opt-in newsletters, communities, or media products
- SaaS features that help users organize, summarize, or act on their own data

## 6. Decision Gates

Before activating a new lane, score it against:

- legality
- consent quality
- data provenance
- terms-of-service fit
- margin potential
- automation potential
- repeatability
- defensibility
- time to cash

If legality, consent, provenance, or terms-of-service fit are weak, reject the lane.

## 7. Orange Data Mining / Data Analysis Constraint

Analysis tools may be used only on compliant data. They are suitable for:

- clustering opted-in leads
- segmenting customer-owned CRM exports
- cleaning public or licensed datasets
- ranking opportunities and operational records

They must not be used to operationalize private-data harvesting or resale.
