# Financial System Compliance Pack

This policy is the mandatory guardrail reference for the Agentic Financial System program.

## 1) Disallowed Activities
- Selling, renting, or brokering harvested personal email lists.
- Scraping private contact data from inboxes for third-party resale.
- Sending unsolicited bulk outreach without lawful basis, sender identity, and unsubscribe.
- Automated financial transfers or live trading execution without explicit approval checkpoints.

## 2) Required Controls
- Consent ledger required for all outbound contact campaigns.
- Suppression list must be applied before every send.
- Data minimization: retain only required fields and delete stale data on schedule.
- Financial risk limits must be machine-enforced (position and drawdown caps).

## 3) Outreach Checklist (Must Pass)
- Audience has documented consent or another lawful basis.
- Message includes clear sender identity and purpose.
- One-click unsubscribe is present and tested.
- Complaint/bounce thresholds are below configured limits.

## 4) Trading Checklist (Must Pass)
- Strategy has completed backtest + forward test thresholds.
- Current drawdown is within policy limits.
- Position size <= configured max risk per trade.
- Stop-loss and max daily loss controls are active.

## 5) Escalation
Any failed check pauses the workflow and creates an incident entry in the mission diary before restart.

