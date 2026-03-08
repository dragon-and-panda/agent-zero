# Compliance Pack: Financial Automation and Data Use

This policy pack defines non-negotiable rules for autonomous workflows related to data extraction, monetization, and capital management.

## 1) Data and Privacy Guardrails

- Use only data the operator is authorized to access.
- Collect and process personal data only with clear consent and a documented lawful basis.
- Do not scrape private inboxes, accounts, or systems without explicit permission.
- Do not build, buy, sell, or share third-party email lists without verified opt-in consent.
- Maintain suppression lists and honor unsubscribe requests immediately.
- Store only minimum necessary personal data and define retention windows.

## 2) Outreach and Messaging Rules

- Follow anti-spam and privacy laws in target regions (for example CAN-SPAM, GDPR, and local equivalents).
- Include sender identity and easy unsubscribe controls in outbound campaigns.
- Keep evidence of consent and campaign logs for auditing.
- Block workflows that attempt bulk unsolicited outreach.

## 3) Monetization Boundaries

- Allowed: affiliate offers, consulting, productized services, digital products, sponsorships, and opt-in newsletters.
- Prohibited: sale of non-consensual contact data, deceptive funnels, impersonation, and fraudulent claims.
- Require transparent disclosures for affiliate or paid promotions.

## 4) Trading and Capital Risk Controls

- Begin with paper trading and backtesting before live deployment.
- Use fixed risk limits per trade and daily drawdown limits.
- Ban martingale and unlimited leverage strategies.
- Keep a written strategy, entry/exit logic, and post-trade review.

## 5) Funds Handling

- Keep transfers auditable with timestamped logs.
- Require manual confirmation for withdrawals and external transfers.
- Use a two-step check for destination account details before sending funds.

## 6) Content and Documentation Standards

- Every sprint updates:
  - mission journal (`docs/programs/<mission>/journal.md`)
  - improvement backlog (`docs/programs/<mission>/improvements.md`)
  - key metrics snapshot (`logs/reports/<week>.md`)
- Publish only truthful, non-deceptive educational content.

## 7) Enforcement Hooks

- Compliance Guardian halts any workflow that includes:
  - unauthorized data harvesting
  - list brokering or sale of personal contacts
  - spam automation
  - unsafe or unbounded trading behavior

If a workflow is paused, it must be revised and re-approved against this pack before restart.
