# Strategy Intake Queue

Use this file as the front door for new autonomous opportunities before implementation starts.

## Intake rules

Every new idea should include:

- a plain-language description,
- the intended customer or buyer,
- the data sources involved,
- whether consent is explicit,
- expected value exchange,
- why the workflow is allowed under platform and data-use rules.

If any of those fields are missing, the item is incomplete and should not move forward.

## Queue

### Candidate: mailbox productivity assistant

- Description: Help an operator search and summarize their own inbox, extract tasks, and organize follow-up work.
- Buyer: solo operators and small teams.
- Data sources: operator-owned mailbox export or authorized API connection.
- Consent status: explicit account-owner authorization required.
- Value exchange: saves time, improves responsiveness, reduces missed commitments.
- Initial view: eligible for scoring.

### Candidate: subscription research brief engine

- Description: Build recurring niche market reports from lawful sources.
- Buyer: operators in narrow verticals.
- Data sources: public-nonpersonal, licensed, or operator-owned sources.
- Consent status: not dependent on personal contact data.
- Value exchange: timely intelligence in a reusable format.
- Initial view: eligible for scoring.

### Rejected example: email list brokerage from mailbox or file extraction

- Description: compile and sell email addresses sourced from inboxes, files, or scraped records.
- Buyer: third-party marketers or online services.
- Data sources: personal contact data with unclear or absent permission for resale.
- Consent status: insufficient.
- Value exchange: weak and privacy-invasive.
- Initial view: reject immediately under `docs/policies/compliance_pack.md`.
