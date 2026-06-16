# Strategy Intake Queue

Capture proposed ventures here before execution.

| Idea | Summary | Status | Notes |
| --- | --- | --- | --- |
| opt-in research newsletter | publish niche insights and monetize through subscriptions, sponsors, or services | PASS | requires a clear signup flow and privacy notice |
| first-party CRM hygiene service | clean, deduplicate, and segment consenting business contact data | PASS | use `consent_contact_extract` and retain provenance |
| owner-authorized inbox assistant | summarize and route a mailbox owner's support or sales inbox | HOLD | confirm access scope, retention, and approved use |
| compiled Gmail email resale | extract email addresses from inboxes and sell the list | REJECT | violates the compliance pack |

## Review checklist

1. run `instruments/strategy/score.sh`
2. run `revenue_planning` for monetization-sensitive ideas
3. attach source, consent, and platform-risk notes
4. advance only PASS items or HOLD items with documented controls
