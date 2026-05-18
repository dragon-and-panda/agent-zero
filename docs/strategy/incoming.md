# Strategy Intake Queue

Use this queue for candidate revenue lanes before activation.

## Active Candidates

| Idea | Status | Why it is attractive | Current concern | Next move |
| --- | --- | --- | --- | --- |
| Inbox-to-CRM assistant for owner-authorized mailboxes | active-review | Recurring service revenue, clear customer value, high automation fit | Must keep strict consent and retention boundaries | Specify OAuth/export scope and CRM outputs |
| Autonomous listing concierge | active-review | Existing repo blueprint, service revenue, clear fulfillment path | Needs sharper packaging and success metrics | Convert blueprint into a sellable MVP offer |
| Research briefs for niche operators | active-review | Uses lawful source collection, reusable templates, margin-friendly | Need niche selection and packaging | Choose one vertical and define sample deliverable |
| Workflow audit and implementation retainer | active-review | High-margin service, strong fit for agentic framework | Requires repeatable audit checklist | Draft standard audit intake and report template |

## Rejected Ideas

| Idea | Status | Reason |
| --- | --- | --- |
| Sell compiled email lists from Gmail or local files | rejected | Fails consent, provenance, privacy, and anti-spam standards |
| Broker inbox-derived contacts to online services | rejected | Converts private communications into third-party lead inventory |
| Mass cold outreach based on scraped or ambiguous contact data | rejected | High compliance and platform-abuse risk |

## Review Rule

Do not move an idea from `active-review` to active execution until it clears:

1. `python/tools/revenue_planning.py`
2. `instruments/strategy/score.sh`
3. `docs/policies/compliance_pack.md`
