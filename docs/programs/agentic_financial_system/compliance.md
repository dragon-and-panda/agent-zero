# Agentic Financial System - Compliance Pack

This policy is mandatory for all agents operating under this program.

## A) Prohibited Activities

Agents must not:
- collect or export personal emails without explicit permission,
- sell, rent, or trade personal contact lists,
- run spam campaigns or deceptive outreach,
- bypass authentication, scrape private inboxes, or evade platform controls,
- process sensitive personal data beyond authorized scope.

## B) Approved Data Sources

Only use data that is one of:
1. First-party contacts with documented opt-in.
2. Customer/partner records with contractual processing rights.
3. Licensed third-party datasets with explicit resale/use rights.
4. Internal communications where account owner has granted access.

## C) Gmail + RAG Controls

- Access is OAuth-based and revocable by the account owner.
- Scope minimization: read only labels/folders listed in the run config.
- Retention minimization: store only fields needed for approved objectives.
- PII handling: hash or redact when full identity is not required.
- Every ingestion run writes an audit log entry with timestamp, source, and record count.

## D) Outreach and Marketing Controls

- Require lawful basis and opt-in status before campaign inclusion.
- Enforce unsubscribe and suppression list checks before every send.
- Include clear sender identity and purpose in all messages.
- Respect sender reputation and deliverability limits (rate caps, warmup schedules).

## E) Orange DataScaping Use Policy

- Use Orange for analysis, clustering, dedupe, and data quality only.
- Do not export segments for unlawful resale.
- Keep lineage tags on every dataset: source, consent type, processing date.

## F) Trading and Financial Safety

- Trading must start in simulation mode.
- No live deployment without passing validation thresholds:
  - minimum sample size,
  - max drawdown limit,
  - stable Sharpe-like risk-adjusted metric.
- Set hard stop rules for live operation (daily loss and account drawdown).

## G) Incident Response

If any policy breach is detected:
1. Pause the affected workflow immediately.
2. Preserve logs and generate incident summary.
3. Notify Apex Orchestrator and Compliance Guardian.
4. Apply remediation before resuming automation.

## H) Required Artifacts Per Sprint

- Consent ledger update
- Data processing audit report
- Campaign compliance checklist
- Revenue/cost reconciliation sheet
- Risk report (if trading systems are active)
