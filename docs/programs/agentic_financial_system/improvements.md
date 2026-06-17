# Agentic Financial System Improvement Backlog

## Active priorities

1. Inbox-to-CRM lane
   - Build only against user-owned inboxes with explicit authorization.
   - Normalize inbound leads, extract structured intent, and push into a first-party CRM.
   - Score by conversion lift, accuracy, operator review burden, and privacy posture.

2. Autonomous listing lane
   - Reuse the listing-service blueprint for lawful marketplace optimization.
   - Focus on pricing, image quality, listing completeness, and response-time automation.
   - Keep platform-policy mappings per marketplace before any outbound automation.

3. Research-product lane
   - Package high-value research, market maps, or workflow playbooks into sellable digital products.
   - Prioritize products that can be generated from public, licensed, or first-party data.

## Improvement queue

### Compliance and risk
- Add a watchdog extension that flags prompts involving inbox scraping, credential misuse, spam, or contact-list resale.
- Inject `docs/policies/compliance_pack.md` into any regulated or monetization workflow before execution.
- Add provenance logging for any dataset referenced by a revenue plan.

### Product and tooling
- Add a first-class `revenue_planning` tool so the agent can screen revenue ideas without immediately trying to execute them.
- Add a mission graph or status dashboard for the active revenue lanes in the web UI.
- Add reusable instruments for opportunity scoring, margin modeling, and weekly reporting.

### Validation
- Define PASS/HOLD/REJECT examples for monetization ideas and keep them in the scoring instrument docs.
- Require explicit operator confirmation before any live integration that touches real customer systems or paid spend.

## Rejected directions
- Selling or brokering personal email lists.
- Non-consensual inbox scraping or email extraction from private sources.
- Any growth tactic that depends on spam, scraping behind access controls, or policy evasion.
