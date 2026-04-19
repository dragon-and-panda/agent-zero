# Strategy Intake Queue

Use this queue for new opportunities before they are pursued by autonomous agents.

## Intake Template

For each idea, capture:

1. name
2. customer and buyer
3. problem being solved
4. delivery mechanism
5. revenue model
6. data sources required
7. consent and provenance status
8. regulatory and platform constraints
9. expected setup cost
10. measurable success criteria
11. next validation step

## Review Procedure

1. Score the idea with `instruments/strategy/score.sh`.
2. Reject any idea that depends on:
   - non-consensual access to inboxes or files
   - spam or unsolicited bulk outreach
   - sale, rental, or brokerage of personal contact data
   - platform abuse or terms-of-service violations
3. Route approved ideas into the charter backlog and journal.

## Current Queue

### Candidate: consented lead-magnet microservice
- Customer and buyer: small B2B operators who need niche research or calculators
- Problem being solved: they need lightweight tooling that captures opted-in prospects
- Delivery mechanism: hosted web app plus downloadable report
- Revenue model: subscription, one-off setup fee, or sponsored placement
- Data sources required: public web pages, customer-provided materials, first-party opt-in forms
- Consent and provenance status: acceptable if explicit consent is recorded for every contact
- Regulatory and platform constraints: privacy notice, unsubscribe flows, records of consent
- Expected setup cost: low to medium
- Measurable success criteria: number of subscribers, conversion rate, retained customers
- Next validation step: ship a narrowly scoped MVP and test demand

### Candidate: inbox scraping and email-list resale
- Status: rejected
- Reason: violates the compliance pack because it depends on personal-data harvesting, likely lacks consent, and creates spam/privacy risk.
