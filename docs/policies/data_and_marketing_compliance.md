# Data and Marketing Compliance Pack

This policy is mandatory for all autonomous workflows touching contact data, outreach, or monetization.

## 1) Allowed Data Collection

- Data from accounts you own/control with valid authorization.
- Data from approved shared mailboxes with explicit admin permission.
- CRM or partner exports with contractually valid usage rights.

## 2) Prohibited Data Collection

- Any unauthorized inbox scraping.
- Credentials sharing or bypassing access controls.
- Collection of sensitive personal data without clear legal basis.

## 3) Consent and Suppression Rules

- Every contact record must include a consent-state field:
  - `opt_in`
  - `legitimate_interest`
  - `suppressed`
  - `unknown`
- `suppressed` contacts are never messaged.
- Unsubscribe and deletion requests must be honored promptly.

## 4) Outreach Rules

- No spam behavior or deceptive messaging.
- Include sender identity and clear opt-out path where required.
- Respect platform terms and local marketing regulations.

## 5) Data Minimization and Retention

- Store only required fields for stated purpose.
- Keep source attribution for auditability.
- Delete stale or unauthorized records on schedule.

## 6) Monetization Rules

- Do not sell raw personal email lists.
- Allowed monetization:
  - Service delivery (research, enrichment, operations).
  - Opt-in audience media/sponsorship.
  - Licensed data products where contract permits resale/use.

## 7) Financial Risk Rules (Trading)

- Trade only after paper/live phased validation.
- Enforce max risk per trade and max daily loss limit.
- Stop automation on drawdown threshold breach.

## 8) Incident Response

If a violation is detected:
1. Pause relevant workflow immediately.
2. Log incident with timestamp and affected records.
3. Notify supervising operator.
4. Remediate and verify before restart.
