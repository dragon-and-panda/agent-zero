# Revenue Compliance Pack

This pack defines the minimum legal, privacy, and platform-safety rules for any autonomous revenue workflow built in this repository.

## Core rule

Revenue systems must be first-party, consent-based, and lawful. If a task depends on privacy invasion, data brokerage, spam, impersonation, or platform evasion, the agent must reject it and propose a compliant alternative.

## Explicitly prohibited

- Harvesting personal email addresses from Gmail, files, exports, inboxes, or third-party systems for resale.
- Selling, brokering, renting, or swapping contact lists, lead lists, or inbox-derived identity data.
- Sending bulk outreach without documented consent or another valid legal basis.
- Accessing inboxes, accounts, or datasets without clear authorization from the owner.
- Bypassing rate limits, anti-bot controls, CAPTCHAs, or marketplace defenses to obtain data or publish spam.
- Building workflows whose primary value comes from violating terms of service or privacy expectations.

## Allowed patterns

- Client-authorized Inbox-to-CRM hygiene:
  - classify inbound mail,
  - extract structured business data from a client-owned mailbox,
  - deduplicate contacts,
  - mark consent status,
  - sync approved records into a CRM.
- Opt-in audience building:
  - lead magnets,
  - newsletter signups,
  - gated reports,
  - waitlists,
  - webinars,
  - referral programs.
- First-party research products built from aggregated or anonymized signals.
- Seller-authorized listing and marketplace automation that follows platform rules.
- Deliverability, routing, and inbox-ops tooling for mailboxes the customer controls.

## Required controls for any email or inbox workflow

1. documented ownership or authorization for the mailbox or data source
2. purpose limitation for each extraction or transformation step
3. data minimization: collect only fields needed for the approved workflow
4. consent tracking for any contact record used in outreach
5. retention and deletion rules for raw message content
6. audit trail showing what was accessed, transformed, and exported

## Decision gates

Before activating a new revenue lane, score it with `instruments/strategy/score.sh`.

- Reject immediately if legality, consent, or data-rights confidence is weak.
- Hold if the workflow is lawful but unclear on margins, automation fit, or time-to-cash.
- Go only when legality, consent, and rights are strong and the economics are reasonable.

## Preferred lane order

1. Inbox-to-CRM Hygiene Service
2. Autonomous Listing Service
3. Research and insight products using first-party or anonymized data
4. Productized automation tooling for client-owned operations

## Safe replacements for rejected ideas

Instead of selling email lists:

- build opt-in lead capture funnels,
- sell CRM cleanup and segmentation,
- offer newsletter operations for publishers with subscriber consent,
- produce anonymized market intelligence,
- run client-owned warm outbound only after consent and legal review.
