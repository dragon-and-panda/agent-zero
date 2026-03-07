# Financial System Compliance Policy

This policy governs all data ingestion, outreach, monetization, and financial activities in the financial system mission.

## 1. Data and Privacy
- Collect only data with explicit user authorization or clearly documented lawful basis.
- Store source provenance and consent status for each contact record.
- Default unknown consent records to `do_not_market`.
- Honor unsubscribe and deletion requests immediately.

## 2. Outreach and Monetization
- Outreach is allowed only to contacts with `explicit_opt_in` status.
- Purchased, scraped, or otherwise non-consensual lists are prohibited.
- Messaging must include identity, purpose, and opt-out mechanism.
- Platform Terms of Service and anti-spam laws are mandatory constraints.

## 3. Security and Access
- Use least-privilege OAuth scopes.
- Protect credentials and tokens in approved secret stores only.
- Log access and changes for auditable review.

## 4. Financial Risk Controls
- No live trading until paper-trading evaluation criteria are met.
- Enforce per-trade risk caps and daily/weekly stop-loss limits.
- Disable strategies that violate drawdown thresholds.

## 5. Governance
- Risk and Compliance agent has authority to block or pause non-compliant workflows.
- All violations must be logged with remediation action and owner.
- Monthly review required for policy updates and legal alignment.
