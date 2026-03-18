# Compliance Pack for Autonomous Revenue Programs

This pack defines the minimum legal, privacy, and ethical controls for any revenue workflow launched from this repository.

## 1. Non-Negotiable Rules

1. **No personal-email brokerage**
   - Do not extract, compile, broker, rent, or sell email addresses taken from private inboxes, sent mail, CC fields, attachments, or other personal correspondence.
   - Do not build or operate spam systems, cold-bulk mail pipelines, or list-resale businesses.
2. **Consent and authorization first**
   - Inbox, CRM, or account-connected data may only be processed with the account owner's authorization and only for the owner's benefit.
   - Use the minimum data required for the task; avoid collecting or persisting full message bodies when summaries or metadata are enough.
3. **First-party and public-source preference**
   - Prefer first-party data, opt-in leads, client-owned CRM records, and public business information over private personal data.
4. **No deceptive outreach**
   - Outreach must be permission-based, accurately represented, and compliant with platform terms, anti-spam laws, and local privacy rules.
5. **Financial controls**
   - Revenue, payouts, and transfers must be recorded in a ledger before disbursement.
   - Transfers to sponsor-controlled accounts should remain reviewable and reversible where possible.
   - If a Cash App destination is used, keep it as a sponsor-controlled, manually verified payout rail until formal finance ops are in place.
6. **Trading is gated**
   - Do not move into live trading until the simulation gate, reserve gate, and risk-limit gate have all passed.

## 2. Allowed Revenue Patterns

The following patterns are in scope:

- **Inbox-to-CRM Hygiene Service**
  - Use RAG over a sponsor's own Gmail or exported mailbox to summarize relationships, deduplicate contacts, extract opt-in business contacts, and draft follow-ups for sponsor review.
  - Orange Data Mining / Orange workflows may be used to segment sender domains, cluster relationship types, and detect stale opportunities.
- **Autonomous Listing Service**
  - Create, improve, and syndicate listings for goods or services under platform-compliant terms.
- **Research and content products**
  - Publish guides, templates, case studies, and video/course assets built from original work.
- **Public-source lead research**
  - Build prospect lists from lawful public business sources, with suppression rules and documented provenance.
- **Simulation-first trading research**
  - Study strategies and paper-trade them with explicit drawdown limits before any live capital is used.

## 3. Prohibited Patterns

The following requests must be rejected or reframed:

- Selling contact lists derived from private inboxes.
- Harvesting personal emails from received/sent/CC archives for resale.
- Unsolicited mass outreach using scraped personal data.
- Accessing third-party accounts without clear authorization.
- Routing funds through undisclosed, unlogged, or unverified rails.

## 4. Required Controls Per Workflow

Every active revenue lane must define:

- **Purpose**: what business outcome the workflow supports.
- **Data boundary**: exactly which data sources are allowed.
- **Lawful basis / authorization**: why the system is permitted to use the data.
- **Human approval points**: when a sponsor must approve action.
- **Suppression rules**: who must not be contacted or retained.
- **Retention policy**: how long summaries, contact records, and artifacts persist.
- **Kill switch**: how the lane is paused when risk spikes.

## 5. Readiness Gates

Before activating any lane, verify:

1. The lane scores **GO** on `instruments/strategy/score.sh`.
2. A compliant acquisition path exists.
3. Delivery artifacts and acceptance criteria are documented.
4. Logging and rollback steps are defined.
5. Payout handling is auditable.

## 6. Default Reframes for Risky Requests

If a request asks for private-contact resale or spam-like acquisition, convert it into one of these compliant alternatives:

- Personal email resale -> **consent-based Inbox-to-CRM cleanup for the account owner**
- Scraped cold outreach -> **public-source business prospect research with suppression controls**
- "Make money fast" with no deliverable -> **small fixed-scope service offer with documented output**
- Immediate live trading -> **paper-trading lab with objective pass/fail thresholds**

## 7. Escalation Conditions

Pause the workflow and escalate when any of the following appear:

- Unclear ownership of mailbox or dataset
- Request to sell or share private contact data
- Platform terms appear to prohibit the planned automation
- Revenue lane requires credentials or payment actions not yet governed
- Strategy drawdown exceeds the documented limit

This pack is the default policy bundle for autonomous financial-system missions. Any ambiguity should be resolved in favor of privacy, legality, and sponsor-auditable operations.
