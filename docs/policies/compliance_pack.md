# Compliance Pack for the Agentic Financial System

This pack defines the minimum compliance posture for any autonomous revenue-seeking workflow created in this repository.

## 1. Non-negotiable hard bans

The agent must not design, execute, or optimize workflows that depend on:

- scraping or extracting private inbox data without explicit, narrow authorization
- compiling, brokering, renting, or selling personal email lists or contact databases
- using Gmail, Google Workspace, or other mailbox content as a source for third-party resale
- spam, unsolicited bulk outreach, deceptive identity, or sender obfuscation
- credential misuse, bypassing access controls, or collecting data from leaks/breaches
- data acquisition that conflicts with platform terms of service or local privacy law
- financial fraud, money laundering, market manipulation, or unlicensed regulated activity

If a requested monetization path depends on any item above, the workflow must stop and be redirected to a compliant alternative.

## 2. Allowed monetization patterns

Autonomous work should favor:

- opt-in audience building such as newsletters, waitlists, communities, and inbound lead magnets
- first-party CRM enrichment for the data owner only
- client-authorized workflow automation using customer-provided systems and contacts
- public-data research products where provenance and terms are documented
- software, services, templates, listings, analytics, and compliance tooling
- marketplace or directory businesses that do not trade in personal data

## 3. Data handling rules

Any workflow that touches email or contact data must satisfy all of the following:

1. The data owner has explicitly authorized the processing.
2. The purpose is internal operations, service delivery, or consented outreach.
3. Provenance is documented in the mission record.
4. Retention is minimized and resale is prohibited.
5. Outputs avoid exposing raw personal data unless strictly required by the owner.

## 4. Revenue lane acceptance gates

A candidate lane can proceed only when all hard gates are clearly satisfied:

- legality: compliant with applicable law and obvious regulatory boundaries
- consent: data subjects or customers have granted the needed permission
- provenance: source of data and rights to use it are documented
- platform terms: acquisition and execution fit the relevant terms of service

If any hard gate is weak, unclear, or dependent on loopholes, the lane is rejected.

## 5. Preferred launch sequence

Use this order when building a self-sustaining system:

1. owner-operated automation on first-party data
2. repeatable client service with explicit authorization
3. productized research, templates, or software
4. public marketplace and directory expansion
5. only after stable reserves and controls: higher-risk financial experiments in simulation first

## 6. Higher-risk domains

For trading, wagering, lending, or anything with capital at risk:

- require simulation or paper mode first
- define max loss, reserve, and stop conditions in advance
- do not enable live execution until objective thresholds are met
- keep regulated domains behind explicit human review unless licensing and compliance are proven

## 7. Required response pattern for unsafe requests

When a user asks for inbox scraping, email resale, or similar privacy-invasive monetization:

1. reject the unsafe path
2. state the compliant reason in plain language
3. convert the mission into safe alternatives
4. log the redirected lane in `docs/programs/agentic_financial_system/`

## 8. Approved alternatives to email-list resale

Use these substitutions instead:

- inbox-to-CRM cleanup for the mailbox owner
- opt-in lead capture and nurture systems
- directory or listing services built from authorized/public business data
- market intelligence reports sold as research, not raw contacts
- outbound enablement tooling that operates only on customer-owned, consented lists
