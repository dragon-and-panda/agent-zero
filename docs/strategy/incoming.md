# Incoming Opportunity Triage

This file is the intake queue and decision rubric for new revenue ideas. Each item should be scored with `instruments/strategy/score.sh` before any build or launch work begins.

## Decision Labels

- `GO`: Legal, consent-based, automatable, and commercially sensible.
- `HOLD`: Potentially valid, but blocked by missing assets, proof, approvals, or instrumentation.
- `REJECT`: Privacy-invasive, deceptive, unlawful, or too risky relative to upside.

## Quick Triage Questions

1. Is the data source first-party, public, or properly licensed?
2. Is every communication channel consent-based or otherwise lawfully permitted?
3. Can the offer be described honestly without inflated earnings or false scarcity?
4. Is downside capped if demand, tooling, or pricing assumptions are wrong?
5. Can the workflow be monitored with logs, metrics, and stop conditions?

If any answer is "no", do not launch until fixed.

## Current Queue

| Idea | Status | Why |
| --- | --- | --- |
| Sell email lists derived from inbox data | REJECT | Violates the compliance pack: personal data brokerage, lack of consent, spam risk, and high legal exposure |
| Consent-based Inbox-to-CRM Hygiene Service | GO | Uses owner-authorized data to create direct operational value |
| Newsletter cleanup and deliverability audit for opt-in senders | GO | Clear customer pain, service revenue, reusable tooling |
| Public-data lead research with manual compliance review | HOLD | Possible, but requires a stricter sourcing and outreach policy |
| Autonomous Forex trading with live capital | HOLD | Requires a dedicated regulated-finance policy pack, simulation first, and human risk approval |
| Tutorial/course on building compliant AI automations | GO | Supports audience growth, product sales, and sponsorship revenue |

## Recommended Revenue Sequence

### Phase 0 - Foundation
- Publish the compliance pack and mission charter.
- Build the scoring instrument and launch checklist.
- Define telemetry for demand, delivery quality, margin, and churn.

### Phase 1 - Fastest Ethical Revenue
- Offer inbox cleanup, CRM deduplication, and follow-up workflow setup to businesses that own the mailboxes.
- Package the work as a fixed-scope service with documented before/after metrics.
- Use each engagement to produce reusable SOPs, templates, and case studies.

### Phase 2 - Productize
- Convert repeated service steps into micro-tools, playbooks, or a lightweight SaaS workflow.
- Sell templates, tutorials, and implementation packages.
- Add affiliate or partner revenue only when the recommendation is genuinely useful.

### Phase 3 - Audience and Distribution
- Publish transparent build logs, tutorials, and short-form educational content.
- Turn case studies into a course and newsletter.
- Use opt-in lead magnets rather than purchased or scraped contacts.

### Phase 4 - Higher-Risk Expansion
- Research simulated trading only after core operating revenue is stable.
- Create a dedicated finance policy pack before any live capital deployment.

## Contingencies

- If service demand is weak: narrow to a clearer niche such as agencies, recruiters, or founder-led SaaS teams.
- If delivery is too manual: pause acquisition and automate the biggest time sink before scaling.
- If compliance is ambiguous: classify as `HOLD` and document the missing controls.
- If a channel underperforms for two review cycles: reallocate effort to the highest-scoring channel with lower downside.
