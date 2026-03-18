# Compliance Pack for Autonomous Revenue Programs

This policy pack defines the minimum legal, privacy, and risk controls for any
autonomous monetization workflow built in this repository.

## 1. Hard prohibitions

The system must not:

- scrape, compile, broker, rent, or sell personal email lists
- extract contacts from inboxes for resale or unsolicited outreach
- send spam, deceptive cold outreach, or messages without a lawful basis
- access Gmail, Google Workspace, or other inbox data unless the account owner
  has explicitly authorized the workflow and the use is documented
- represent speculative trading as guaranteed income
- deploy live trading before paper-trading and risk gates are satisfied
- auto-route funds to a payment destination without verifying ownership,
  platform terms, and accounting controls

Any request that depends on personal-data resale, inbox harvesting without
consent, or deceptive acquisition is a REJECT lane.

## 2. Approved patterns

The system may support:

- consent-based Inbox-to-CRM hygiene for a client using the client's own
  mailbox or export
- deduplication, contact normalization, and consent-status tagging for a
  first-party CRM
- marketplace listing, research, documentation, or content businesses that use
  lawful data sources
- opt-in newsletters, lead magnets, and public-content funnels
- simulation-first research into trading or capital allocation

When inbox data is processed, outputs must stay with the client that owns the
source data. No resale, no cross-client mixing, and no shadow copy for future
marketing use.

## 3. Data handling rules

- Keep only the minimum fields needed for the approved workflow.
- Prefer company-role or first-party CRM records over personal-contact data.
- Track provenance for each dataset: source, owner, consent basis, and purpose.
- Delete or rotate temporary exports after the contracted workflow completes.
- Use analytics tools such as Orange Data Mining only for internal
  organization, segmentation, or deduplication of authorized datasets.

## 4. Revenue-lane gating

Before a lane is activated, it must pass:

1. legality review
2. consent/privacy review
3. downside review
4. unit-economics review
5. operational redundancy check

Use `instruments/strategy/score.sh` to classify lanes as GO, HOLD, or REJECT.

## 5. Financial risk controls

### 5.1 Trading and speculation

Trading is a late-stage lane only. Requirements:

- paper-trading first
- written strategy and risk rules
- reserve capital kept outside the trading account
- maximum daily and weekly drawdown limits
- post-trade journaling and review

No live trading if any of the above controls are missing.

### 5.2 Payout operations

- Keep payout routing manual or separately audited.
- Do not hard-code personal payment handles in repo docs, prompts, or scripts.
- Reconcile every payout against an invoice, platform statement, or contract.

## 6. Escalation rules

Escalate to the Risk and Ethics Governor if a workflow:

- touches personal communications or regulated financial activity
- proposes mass messaging or list resale
- cannot prove consent or ownership of the data
- relies on "guaranteed profit" framing or undefined downside

If escalation is triggered and the issue is unresolved, the lane remains HOLD or
REJECT.
