# Strategy Intake Queue

Use this queue to capture revenue ideas before any building or automation work starts.

## Required fields

- Idea
- Customer
- Offer
- Acquisition path
- Data provenance
- Consent model
- Platform exposure
- Notes

## Queue

### Rejected

#### Contact-list brokerage from email or local files
- Idea: extract email addresses from Google email data and other files, then sell the lists.
- Decision: reject.
- Reason: personal-data resale, weak consent, unclear provenance, and high anti-spam risk.
- Safe replacement: first-party inbox-to-CRM cleanup for the account owner or an authorized client.

### Candidate

#### First-party inbox-to-CRM operations
- Customer: mailbox owner or authorized client
- Offer: convert first-party inbox activity into CRM records, follow-up tasks, and summaries
- Acquisition path: direct consulting or productized setup
- Data provenance: first-party
- Consent model: explicit customer authorization
- Platform exposure: low if kept inside user-owned systems

#### Productized research briefs
- Customer: operators in a narrow niche
- Offer: curated market maps, workflow audits, and actionable research
- Acquisition path: subscriptions or one-off reports
- Data provenance: public or licensed
- Consent model: not based on personal-data extraction
- Platform exposure: low

#### Autonomous listing operations
- Customer: inventory owner
- Offer: listing creation, syndication, and message handling
- Acquisition path: service fee or software subscription
- Data provenance: customer-owned inventory data
- Consent model: explicit customer authorization
- Platform exposure: medium, depends on marketplace rules
