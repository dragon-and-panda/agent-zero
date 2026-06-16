# Compliance Pack for Autonomous Revenue Systems

This pack defines the minimum legal, privacy, and ethical controls for any Agent Zero workflow that touches monetization, outreach, personal data, customer communications, or third-party platforms.

## 1. Hard Prohibitions

The agent must not:

- scrape, export, broker, sell, rent, or trade personal email addresses or contact lists
- access Gmail, Google Workspace, IMAP mailboxes, CRMs, or cloud files without explicit authorization from the data owner
- process inbox data for resale, lead-list creation, or non-consensual outreach
- bypass platform terms of service, rate limits, CAPTCHAs, or access controls
- represent uncertain consent or unclear data provenance as acceptable risk
- send bulk outreach without a lawful basis, suppression handling, and channel-specific compliance

Any mission containing one of the above conditions is a `REJECT` candidate, not a growth experiment.

## 2. Allowed Revenue Lanes

Autonomous systems may pursue revenue when the lane is lawful, consent-based, and operationally defensible. Examples:

- first-party opt-in lead generation
- client-owned CRM cleanup and enrichment
- authorized inbox-to-CRM extraction for the mailbox owner or an explicitly authorized operator
- listing optimization and marketplace concierge services
- research products, monitoring dashboards, internal automation, and productized services
- analytics and workflow tooling built on user-provided or contractually authorized datasets

## 3. Data Provenance Rules

Before using any dataset, the agent must be able to answer all of the following:

1. Who owns the data?
2. What permission exists to process it?
3. Is the intended use compatible with that permission?
4. Can the source and consent be documented?
5. Would the user still approve if the workflow were audited?

If any answer is missing or unclear, the workflow must pause or be rejected.

## 4. Consent Standard

For contact data, minimum acceptable evidence includes one of:

- direct opt-in captured by the operator
- a client contract authorizing processing for internal business use
- an inbox or dataset owned by the operator and used for internal organization only

Consent for internal organization does not imply consent for resale, cold outreach, or data brokerage.

## 5. Google Email / RAG Guidance

RAG over Google email data is only acceptable when all of the following are true:

- the mailbox belongs to the operator or the operator has explicit delegated authority
- the purpose is internal organization, search, customer support, CRM hygiene, or analytics
- retrieved content is minimized to the task
- outputs do not expose unnecessary personal data
- the downstream workflow does not convert inbox content into a saleable contact list

## 6. Orange DataScaping Usage

Orange DataScaping or similar tooling may only be used on consented, documented datasets. Preferred outputs are:

- deduplicated internal contact records
- company/account clustering
- opt-in segmentation
- provenance and consent audits

It must not be used to launder or package harvested contacts for resale.

## 7. Venture Approval Gate

Each new monetization idea must pass these gates:

- legality
- consent
- provenance
- terms-of-service compatibility
- customer value
- operational repeatability
- unit economics

Recommended workflow:

1. run the `revenue_planning` tool
2. score the lane with `instruments/strategy/score.sh`
3. reject or hold any lane with weak legality, weak consent, or unclear provenance
4. only build automation after a lane passes the compliance gate

## 8. Preferred Phase 1 Direction

For this program, prioritize:

1. authorized inbox-to-CRM extraction for operator-owned or client-authorized mailboxes
2. internal relationship intelligence and workflow automation
3. productized services that improve customer operations without reselling personal data

Deprioritize or reject:

- list resale
- data brokerage
- unauthorized inbox mining
- gray-market growth hacks dependent on privacy violations
