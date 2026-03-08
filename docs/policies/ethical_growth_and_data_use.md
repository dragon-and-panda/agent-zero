# Ethical Growth and Data Use Policy

This policy applies to all autonomous workflows in the Ethical Financial System program.

## 1) Allowed Data Operations
- Process only data from accounts and files that are owned or explicitly authorized by the operator.
- Store minimal data required for the task.
- Prefer metadata and derived features over raw personal content.

## 2) Prohibited Actions
- No scraping, purchasing, selling, renting, or sharing personal email lists.
- No unauthorized account access, credential abuse, or bypassing consent.
- No deceptive outreach, identity misrepresentation, or hidden commercial intent.

## 3) Outreach Compliance Requirements
- Use consent-based contacts only.
- Include sender identity and unsubscribe mechanism in outbound campaigns.
- Honor unsubscribe/suppression requests immediately.
- Maintain campaign logs for auditability.

## 4) Financial Risk Requirements
- Do not represent strategies as guaranteed profit.
- Require paper-trade validation before live capital deployment.
- Enforce hard risk limits: per-trade risk, daily loss cap, and leverage ceiling.

## 5) Operational Controls
- All automations must emit telemetry logs.
- High-risk actions require dual validation:
  - compliance check passed
  - finance/risk check passed
- Incidents are documented in the mission diary with remediation steps.

## 6) Enforcement
- Workflows violating this policy are paused.
- Repeated violations trigger mandatory prompt and instrument updates before restart.
