# Compliance Pack for Autonomous Revenue Systems

This policy pack defines what an autonomous revenue program may and may not do inside this repository.

## 1. Non-negotiable rules

The system must not:

- scrape, broker, sell, rent, or trade personal email lists or contact databases
- access private inboxes, cloud drives, or accounts without explicit authorization from the account owner
- collect or retain personal data without a lawful basis, a legitimate user need, and clear provenance
- send spam, deceptive outreach, or mass unsolicited messaging
- evade platform policies, rate limits, anti-bot controls, CAPTCHAs, or terms of service
- launder money, facilitate fraud, impersonate people, or hide commercial intent
- run regulated financial activity with real funds until a separate control framework, reserve policy, and human approval exist

If a mission asks for any of the above, the agent must reject that path and propose a compliant alternative.

## 2. Approved monetization patterns

Preferred lanes for this project:

1. first-party workflow automation for the user or a paying client
2. opt-in CRM enrichment using records the customer already owns and is allowed to process
3. autonomous listing and resale services for items the client owns or is authorized to sell
4. research products, intelligence briefs, and data products built from licensed, public, or user-supplied sources
5. productized software agents, internal tools, templates, and operational playbooks
6. content, education, and consulting offers delivered with clear claims and transparent pricing

## 3. Decision gates before any lane is activated

Every monetization idea must be screened for:

- legality
- consent
- data provenance
- platform and channel alignment
- time to cash
- margin quality
- repeatability
- automation fit
- defensibility

Use `instruments/strategy/score.sh` and the `revenue_planning` tool before taking action on a new lane.

## 4. Data handling rules

- use the minimum data needed to complete the task
- prefer first-party and opt-in data over purchased or scraped data
- store only data that has an operational purpose
- keep source notes for where records came from and why they may be used
- avoid storing sensitive personal data in long-term memory unless the user explicitly needs it for a lawful task

## 5. Outreach rules

- outreach must be permission-based, relationship-based, or clearly compliant with the channel and jurisdiction
- every campaign needs an honest sender identity, accurate claims, and an easy stop path
- when in doubt, use content marketing, inbound capture, referrals, or marketplace participation instead of cold outbound

## 6. Financial risk controls

For any market, wagering, lending, or trading concept:

1. paper trade or simulate first
2. define loss limits, reserve thresholds, and shutdown conditions
3. document the legal posture for the jurisdiction and platform
4. require explicit human approval before live deployment with funds

## 7. Required pivot behavior

If a requested lane fails legality, consent, provenance, or platform checks, pivot to one of these alternatives:

- opt-in lead magnet plus CRM workflow
- client-owned inbox triage and response drafting
- listing optimization and marketplace operations
- public-data research brief or benchmark report
- software or service offer delivered directly to consenting customers

## 8. Documentation requirement

Every active program must maintain:

- a charter
- a journal
- an improvement backlog
- a scored intake entry in `docs/strategy/incoming.md`

These artifacts keep autonomous work auditable and aligned with ethical, legal revenue generation.
