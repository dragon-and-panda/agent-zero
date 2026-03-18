# Strategy Intake and Routing

Use this document to classify new missions before agents spend effort on them.

## Intake Template

Record new ideas in this format:

```text
Mission:
Goal:
Primary buyer:
Data sources:
Allowed actions:
Disallowed actions:
Expected deliverable:
Fastest path to cash:
Primary risk:
Backup lane:
```

## Routing Rules

- **GO**: lawful, consent-based, fast-to-deliver, and can be executed with current assets.
- **HOLD**: potentially useful, but blocked on missing controls, missing assets, or excess capital/risk.
- **REJECT**: violates privacy, consent, platform rules, or the compliance pack.

## Examples

### GO — Consent-Based Inbox-to-CRM Hygiene Service

```text
Mission: Convert the sponsor's authorized Gmail data into a clean CRM and follow-up queue
Goal: Recover warm opportunities and create a paid cleanup deliverable
Primary buyer: Sponsor or client who owns the mailbox
Data sources: Gmail export/API, existing CRM, sponsor notes
Allowed actions: summarize relationships, deduplicate contacts, segment with Orange, draft follow-ups for review
Disallowed actions: sell contacts, share private addresses, send mass unsolicited outreach
Expected deliverable: CRM table + opportunity report + draft reply queue
Fastest path to cash: fixed-fee inbox cleanup package
Primary risk: privacy scope creep
Backup lane: Autonomous Listing Service
```

### GO — Autonomous Listing Service

```text
Mission: Improve and publish listings for inventory or client goods
Goal: Generate near-term cash flow from listing operations
Primary buyer: sponsor inventory or external seller clients
Data sources: seller-supplied photos, notes, platform rules, public comps where permitted
Allowed actions: enhance images, write listings, publish through compliant adapters
Disallowed actions: policy-breaking automation, fake scarcity claims
Expected deliverable: live listings + response scripts
Fastest path to cash: per-listing or success-fee package
Primary risk: platform friction
Backup lane: content products
```

### HOLD — Trading Before Readiness Gates

```text
Mission: deploy capital into live Forex immediately
Goal: grow funds through trading
Primary buyer: internal treasury
Data sources: market feeds, strategy notebooks
Allowed actions: research, backtest, paper trade
Disallowed actions: live trading before reserve and simulation thresholds are met
Expected deliverable: paper-trading report and pass/fail metrics
Fastest path to cash: none until promotion gate passes
Primary risk: capital loss
Backup lane: keep revenue lanes A-C active
```

### REJECT — Personal Email List Brokerage

```text
Mission: compile email addresses from inbox data and sell the list
Goal: monetize private contact data
Primary buyer: list resellers / third-party senders
Data sources: received mail, sent mail, CC fields, attachments
Allowed actions: none
Disallowed actions: extraction for resale, spam, private-contact brokerage
Expected deliverable: none; request rejected
Fastest path to cash: non-compliant
Primary risk: privacy, legal, and platform violations
Backup lane: reframe as sponsor-owned Inbox-to-CRM cleanup
```

## Default Prioritization

When several GO ideas exist, prioritize in this order:

1. compliant lane with the shortest delivery cycle,
2. lane that reuses existing assets and tools,
3. lane that improves acquisition for another lane,
4. lane that requires new capital only after earlier lanes are producing.
