# Compliance Pack: Ethical Financial Automation

This policy pack defines non-negotiable guardrails for autonomous workflows that handle personal data, outreach, monetization, and financial operations.

## 1) Hard Prohibitions

- Do not scrape, broker, or sell personal email lists.
- Do not use leaked, purchased, or unverified contact databases.
- Do not automate spam, phishing, impersonation, or deceptive outreach.
- Do not bypass platform terms of service, paywalls, anti-bot protections, or account safeguards.
- Do not provide unlicensed financial advice or promise investment returns.

## 2) Allowed Contact Data Sources

Only process contact records that are one of:

1. First-party, user-owned data exports (for example, the operator's own mailbox export).
2. Explicit opt-in form submissions.
3. Contracted partner data with written processing authorization.

Every record must include a `consent_status` field and a source trace.

## 3) Consent and Outreach Rules

- Outreach is allowed only when consent or legal basis is documented.
- Include easy unsubscribe and honor removals immediately.
- Maintain suppression lists and never re-add removed contacts without renewed consent.
- Use domain and frequency throttling to avoid spam-like behavior.

## 4) Data Retention and Security

- Keep only the minimum fields needed for the stated objective.
- Encrypt stored exports and logs containing personal data.
- Set retention windows and automated deletion jobs.
- Log all data reads/writes for auditability.

## 5) Monetization Safety Rules

- Revenue generation must use lawful models (opt-in newsletters, affiliate content, consulting, products, compliant B2B lead programs).
- Any list-based service must use consent-verified records and documented client terms.
- Never position personal data itself as the product.

## 6) Trading and Capital Deployment Controls

- Start with paper trading and risk simulations before real funds.
- Use fixed position sizing, hard stop-losses, and max daily drawdown rules.
- Record strategy assumptions, backtests, and post-trade reviews.
- Route realized profits through declared business accounting workflows.

## 7) Escalation Triggers

Pause all automations and escalate to human review when:

- consent provenance is missing or ambiguous,
- outreach complaint rates spike,
- a workflow requests prohibited data acquisition,
- a strategy violates risk caps,
- legal/compliance uncertainty is detected.

## 8) Audit Checklist (per release)

- [ ] Data source inventory updated
- [ ] Consent schema validated
- [ ] Suppression pipeline tested
- [ ] Outreach templates include unsubscribe language
- [ ] Financial risk limits validated
- [ ] Incident rollback procedure tested
