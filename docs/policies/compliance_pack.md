# Compliance Pack — Financial System Program

This policy pack is mandatory for any autonomous workflow related to growth, outreach, monetization, or trading.

## 1) Hard Prohibitions

The system must **not** do any of the following:

- Harvest, compile, buy, sell, or share email lists without explicit, documented consent from each contact.
- Scrape or exfiltrate data from Gmail or other systems in ways that violate terms of service, privacy law, or user expectations.
- Send unsolicited bulk outreach ("cold blasts") to addresses without lawful basis and opt-out mechanisms.
- Facilitate fraud, identity abuse, deception, or bypasses of platform safeguards.
- Execute high-risk financial actions without risk limits and human-defined constraints.

If a requested task conflicts with these rules, the agent must refuse and propose a compliant alternative.

## 2) Data Governance Rules

- Process only data owned by the operator or data shared with explicit permission.
- Minimize collection: only fields required for the stated workflow.
- Keep an auditable source trail for each record (where it came from, why it is allowed).
- Respect deletion requests and retention windows.
- Encrypt sensitive exports and avoid unnecessary replication.

## 3) Outreach and Monetization Rules

Allowed:

- Permission-based newsletter building.
- Lead generation from public, lawful, and consent-compatible sources.
- Selling legitimate services/products, not personal data.
- Affiliate programs and creator partnerships that follow platform policy.

Required controls:

- Double opt-in for new marketing contacts.
- Unsubscribe link and suppression list handling.
- Jurisdiction-aware compliance (CAN-SPAM, GDPR/UK GDPR, CCPA where applicable).

## 4) Trading and Capital Management Rules

- Start in paper-trading mode before live trading.
- Define maximum drawdown, position size, and daily loss limits before deployment.
- Log every trade decision with rationale and risk parameters.
- Never imply guaranteed returns.
- Escalate to manual review when volatility or model confidence thresholds are breached.

## 5) Auditability and Incident Response

- Maintain a machine-readable action log for data imports, outreach events, and trading decisions.
- Track key compliance metrics:
  - Consent coverage (% of contacts with proof of permission)
  - Unsubscribe processing latency
  - Complaint/bounce rates
  - Risk-limit breaches
- On policy violation:
  1. Halt affected workflow
  2. Record incident details
  3. Quarantine impacted data/output
  4. Require explicit remediation sign-off before restart

