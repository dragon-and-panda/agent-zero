### revenue_planning:

Evaluate a venture, outreach, or monetization plan against legality, consent, privacy, and platform-risk guardrails.

- **venture_summary**: short description of the business idea
- **data_sources**: where customer, content, or operational data would come from
- **customer_acquisition**: how the venture gets customers
- **automation_plan**: what the agent would automate
- **authorization_status**: who authorized any sensitive data or account access
- **monetization_goal**: how the venture makes money

Use this before executing any revenue strategy that touches contact data, inboxes, outreach, or scraping.

usage:
```json
{
  "thoughts": [
    "I should score this monetization plan before acting."
  ],
  "tool_name": "revenue_planning",
  "tool_args": {
    "venture_summary": "Owner-authorized Gmail assistant for support triage and follow-up drafting",
    "data_sources": "User's own Gmail mailbox and uploaded SOPs",
    "customer_acquisition": "Inbound leads and existing customer support requests",
    "automation_plan": "Summarize threads, tag intent, and draft replies for approval",
    "authorization_status": "Mailbox owner explicitly authorized access",
    "monetization_goal": "Paid support workflow software"
  }
}
```
