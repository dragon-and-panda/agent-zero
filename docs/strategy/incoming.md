# Strategy Intake Queue

Use this file as the front door for new revenue ideas before execution.

## Template

### Idea
- Summary:
- Customer:
- Offer:
- Channel:
- Data sources:
- Approval required:

### Scoring snapshot
- Legality confidence:
- Consent strength:
- Data rights confidence:
- Platform risk:
- Result:

### Notes
- Risks:
- Evidence:
- Next step:

---

## Example: rejected

### Idea
- Summary: Compile email addresses from inboxes and sell the list
- Customer: Third-party marketers
- Offer: Contact database
- Channel: Data brokerage
- Data sources: Private email content
- Approval required: Not applicable

### Scoring snapshot
- Legality confidence: low
- Consent strength: low
- Data rights confidence: low
- Platform risk: high
- Result: REJECT

### Notes
- Risks: privacy violation, spam enablement, likely platform and legal violations
- Evidence: fails the compliance pack on consent and personal-data brokerage
- Next step: replace with an opt-in audience workflow or a first-party digital product offer

---

## Example: approved to plan

### Idea
- Summary: Sell a niche operations template pack with an opt-in newsletter
- Customer: Small online operators
- Offer: Digital templates plus educational email updates
- Channel: Website and compliant marketplace listings
- Data sources: First-party site analytics and subscriber signups
- Approval required: yes before publication

### Scoring snapshot
- Legality confidence: high
- Consent strength: high
- Data rights confidence: high
- Platform risk: low
- Result: PASS

### Notes
- Risks: weak differentiation if positioning is generic
- Evidence: uses first-party opt-in data and ordinary commerce channels
- Next step: run `revenue_planning` and draft the launch checklist
