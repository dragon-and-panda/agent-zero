# Strategy Intake Queue

Use this file as the top-level queue for venture ideas before the agent starts execution.

| Idea | Status | Why |
| --- | --- | --- |
| Owner-authorized inbox RAG for business search, support triage, and CRM memory | HOLD | Viable, but requires explicit mailbox authorization, minimal scopes, retention rules, and no contact resale. |
| Opt-in niche newsletter monetized with sponsorships and affiliate links | PASS | First-party audience building with clear consent and durable monetization paths. |
| Productized automation service for a narrow vertical | PASS | Revenue does not depend on personal-data brokerage and can compound through SOPs and tools. |
| Sell compiled email address lists gathered from inboxes or files | REJECT | Violates privacy, consent, and anti-spam standards. |

## Intake checklist

Before a new idea moves into execution, capture:

1. Revenue mechanism
2. Data sources
3. Consent model
4. Platform dependencies
5. Main failure mode

Then run `instruments/strategy/score.sh` and, when helpful, the `revenue_planning` tool.
