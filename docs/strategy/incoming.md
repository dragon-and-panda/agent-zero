# Strategy Intake Queue

Use this queue for every proposed monetization idea before any build-out work begins.

## Intake Rules

1. Describe the opportunity in one sentence.
2. State the data source and who owns or authorizes it.
3. Identify the intended customer and revenue model.
4. List any likely compliance, privacy, or platform risks.
5. Run `instruments/strategy/score.sh` and record the result.
6. Reject the idea immediately if it depends on prohibited data acquisition.

## Intake Template

```md
## Opportunity Name
- description:
- customer:
- revenue model:
- data source:
- authorization / consent basis:
- key tools or systems involved:
- likely policy or TOS risks:
- score result:
- decision:
```

## Current Queue

### 1. Authorized Inbox-to-CRM Triage
- description: turn a user-owned or client-owned inbox into structured opportunity and support records.
- customer: operators, founders, agencies, or SMB teams with messy inbound email.
- revenue model: service retainer, setup fee, or internal efficiency gain.
- data source: explicitly authorized first-party inbox data.
- authorization / consent basis: owner-authorized processing for internal operations.
- key tools or systems involved: Gmail export or API, RAG, CRM mapping, Orange DataScaping for lawful clustering and cleanup.
- likely policy or TOS risks: must preserve consent status and avoid using extracted contacts for resale or spam.
- score result: pending initial score run.
- decision: candidate priority lane.

### 2. Autonomous Listing Concierge
- description: create and optimize marketplace listings from seller-provided inventory and notes.
- customer: individual sellers, resale operators, or consignment businesses.
- revenue model: listing fee, subscription, or revenue share.
- data source: seller-provided assets and marketplace-compliant integrations.
- authorization / consent basis: owner-provided product data.
- key tools or systems involved: listing pipeline, image enhancement, description generation, marketplace adapters.
- likely policy or TOS risks: must follow channel rules and avoid deceptive listing behavior.
- score result: pending initial score run.
- decision: active hedge lane.

### 3. Niche Research Briefs
- description: deliver paid intelligence briefs using public, licensed, and first-party sources.
- customer: founders, agencies, investors, or operators in specific niches.
- revenue model: one-off reports or subscriptions.
- data source: public information, licensed datasets, and internal synthesis.
- authorization / consent basis: public or licensed use.
- key tools or systems involved: knowledge retrieval, source citation, report generation, quality review.
- likely policy or TOS risks: need source discipline and confidence labeling.
- score result: pending initial score run.
- decision: warm lane.

### 4. Personal Email List Brokerage
- description: compile and sell email lists to online services.
- customer: N/A.
- revenue model: prohibited.
- data source: personal email addresses from mixed or unclear provenance.
- authorization / consent basis: inadequate.
- key tools or systems involved: prohibited workflow.
- likely policy or TOS risks: severe privacy, anti-spam, and platform-abuse exposure.
- score result: reject.
- decision: rejected by policy; do not implement.
