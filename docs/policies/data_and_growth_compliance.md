# Data and Growth Compliance Pack

## Purpose
Define mandatory controls for autonomous growth, contact data handling, outreach, and monetization workflows.

## Prohibited Actions
- Selling, renting, exchanging, or brokering personal email lists.
- Sending unsolicited bulk outreach without documented consent or lawful basis.
- Collecting data from compromised accounts, unauthorized scraping, or bypassing access controls.
- Ignoring unsubscribe requests, suppression flags, or platform anti-spam rules.

## Required Controls
1. **Lawful Basis Registry**
   - Every contact must store legal basis (`consent`, `contract`, `legitimate_interest`, etc.).
   - Missing basis means `do_not_contact=true`.

2. **Consent Ledger**
   - Store source URL/app, opt-in timestamp, consent scope, and evidence hash.
   - Scope violations are blocked pre-send.

3. **Suppression Enforcement**
   - Central suppression list checked before every outbound action.
   - Unsubscribes propagate to all channels within one execution cycle.

4. **Data Minimization**
   - Keep only fields needed for the active workflow.
   - Remove or anonymize stale data on retention schedule.

5. **Provenance and Auditability**
   - Record where each contact attribute was obtained.
   - Keep immutable event logs for extraction, segmentation, and outreach.

6. **Human Escalation Triggers**
   - Complaint spikes, deliverability collapse, legal notices, or anomaly flags pause automation.

## Approved Revenue Modes (Phase 1)
- Opt-in newsletter sponsorship
- Affiliate campaigns with transparent disclosures
- Productized consulting/services
- Digital products (templates, courses, reports)
- SaaS subscriptions

## Trading Risk Gate (Post Phase 1)
- Paper-trading only until minimum stability criteria are met.
- Hard limits for daily drawdown, position size, and risk per trade.
- Strategy deployment requires logged backtest + forward-test evidence.

## Enforcement
Any workflow violating this pack must return `BLOCKED_BY_COMPLIANCE` and write an incident record to mission logs.
