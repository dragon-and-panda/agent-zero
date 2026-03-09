# Financial Data and Outreach Compliance Policy

## Scope
Applies to all workflows under `docs/programs/financial_system/` and any tools/agents touching email, contacts, outreach, or revenue operations.

## 1) Data Access Rules
- Only use data from accounts and systems where explicit authorization exists.
- Limit OAuth scopes to least privilege required for the task.
- Record source system, consent basis, and retrieval time for every ingestion run.

## 2) Consent and Contactability
- Outreach is permitted only when a lawful basis and consent/legitimate-interest criteria are satisfied.
- Maintain and enforce a suppression list for unsubscribe and no-contact requests.
- Never bypass platform anti-spam controls or identity requirements.

## 3) Prohibited Activities
- Selling or brokering raw personal email lists.
- Harvesting contacts from private communications for resale or unsolicited bulk messaging.
- Deceptive marketing, impersonation, phishing, or undisclosed automation.

## 4) Data Governance
- Minimize stored personal data to fields needed for approved workflows.
- Use retention windows; purge stale or disallowed data on schedule.
- Protect sensitive records and restrict access to approved agents/tools.

## 5) Financial Risk Controls
- Trading activity must begin in paper-trading mode and pass predefined metrics before live deployment.
- Define hard limits: max position size, max daily loss, and max drawdown.
- Auto-pause strategy execution when risk thresholds are breached.

## 6) Audit and Incident Response
- Log all outreach batches, recipient source, consent state, and outcome metrics.
- On policy violation: halt workflow, create incident entry, and require human review before restart.
- Review policy monthly and update guardrails as laws/platform rules change.
