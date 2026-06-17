# Opportunity Intake and Triage

Use this page to capture new revenue ideas before agents turn them into active programs.

## Intake template

For each idea, record:

- problem
- target customer
- revenue model
- required data
- proof of data rights
- consent model
- platform dependencies
- time-to-cash hypothesis
- automation potential
- decision after running `instruments/strategy/score.sh`

## Decision rules

- GO: lawful, consent-based, customer value is real, and the workflow is operationally feasible.
- HOLD: likely lawful but missing evidence on customer demand, margins, or data rights.
- REJECT: depends on privacy invasion, unconsented outreach, data brokerage, account abuse, or platform evasion.

## Reference examples

| Idea | Decision | Why |
| --- | --- | --- |
| Consent-based Inbox-to-CRM Hygiene Service for a client-owned Google Workspace mailbox | GO | Strong customer value, clear authorization path, recurring ops work, easy to productize. |
| Autonomous Listing Service for sellers who authorize marketplace posting and buyer messaging guardrails | GO | First-party service revenue, measurable outcomes, existing repo blueprint. |
| Aggregated industry digest built from public sources and client-approved first-party notes | GO | Can become subscription research without selling personal data. |
| Gmail mining to compile personal email lists for resale | REJECT | Privacy invasion, likely unlawful, and misaligned with platform and anti-spam rules. |
| Purchased lead lists plus cold outreach automation | REJECT | Weak consent, high deliverability risk, and poor compliance posture. |
| Gmail RAG used only to triage support mail and draft CRM-ready records for the mailbox owner | HOLD -> GO after authorization proof | Allowed if mailbox ownership, purpose limitation, and retention controls are documented. |

## Email-data rule of thumb

Any mission involving Gmail, mailbox exports, contact books, CSVs, or personal identity data starts in HOLD status until ownership and consent are documented. It becomes REJECT if the planned output is resale, list brokerage, or spam.
