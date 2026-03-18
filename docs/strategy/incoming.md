# Strategy Intake Queue

Use this page as the first stop for new autonomous missions. Each idea should be tagged GO, HOLD, or REJECT before significant build effort begins.

---

## Intake Rubric

Score each opportunity on:

- Legality
- Consent clarity
- Time to first revenue
- Repeatability
- Automation fit
- Margin
- Platform dependence
- Downside risk

Use `instruments/strategy/score.sh` to produce a first-pass decision and then record the final call here.

---

## Current Examples

| Initiative | Status | Why | Safer or better version | Next action |
| --- | --- | --- | --- | --- |
| Compile email addresses from inboxes and sell the lists | REJECT | Personal data brokerage, consent failure, spam risk, and likely policy or legal violations | Replace with a consent-based Inbox-to-CRM Hygiene Service for the mailbox owner | Do not build |
| Analyze customer-authorized mailbox exports in Orange Data Mining to deduplicate contacts into a CRM | GO | Lawful when the customer authorizes access and the output stays with the customer | Add OAuth or CSV import, dedupe rules, and audit logging | Build intake checklist and service SOP |
| Launch autonomous marketplace listing operations for owned or client inventory | GO | Direct service revenue, strong automation fit, existing repo alignment | Reuse the listing service blueprint and expand into retainers | Package offer and pilot with one category |
| Start live Forex trading immediately after first profits | HOLD | High downside, regulated and operationally fragile, poor fit for early cash preservation | Create a paper-trading lab with journal, risk caps, and a research gate before any live capital | Defer until core revenue tracks are stable |
| Route all payouts automatically to a personal Cash App handle | HOLD | Bookkeeping, fraud, tax, and platform compliance risks | Keep payouts in a business processor or reviewed account first, then transfer manually after reconciliation | Define finance workflow |
| Build a tutorial/course and YouTube story around funding a mech suit and robot body | GO | Original content, brand-building, and reusable educational assets | Use an anthropomorphic narrator and document only lawful, repeatable systems | Create content calendar and story bible |

---

## Decision Rules

- **GO:** Legally clean, consent-backed, and operationally simple enough to launch with limited capital.
- **HOLD:** Potentially viable, but missing controls, proof, or prerequisites.
- **REJECT:** Depends on unconsented personal data, deceptive acquisition, platform abuse, or uncontrolled financial risk.

When in doubt, HOLD the initiative until the compliance pack and revenue program both support it.
