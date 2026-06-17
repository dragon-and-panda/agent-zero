# Compliance Pack for Autonomous Revenue Programs

This policy pack governs any autonomous or semi-autonomous workflow in this repository that aims to create, price, market, sell, or support revenue-generating activity.

It is intentionally strict. Revenue is only acceptable when acquisition, processing, and monetization methods are lawful, ethical, consent-based, and consistent with platform terms.

---

## 1. Non-Negotiable Rules

### 1.1 Prohibited data practices
Agents must not:

- harvest email addresses, phone numbers, or other personal identifiers from inboxes, documents, websites, or third-party sources without explicit, documented authorization and a lawful basis;
- compile, enrich, segment, or sell personal contact lists;
- use scraped personal data for cold outreach where consent, legitimate interest analysis, or platform permission is missing;
- bypass access controls, CAPTCHAs, anti-bot systems, rate limits, or terms of service;
- exfiltrate or repurpose data from Gmail, Google Workspace, or any other communications system for resale or brokering.

### 1.2 Human data handling
Any workflow touching human communications or personal data must have:

- a documented purpose;
- a known data owner;
- a lawful basis for processing;
- data minimization;
- a retention/deletion rule;
- a review path for incidents and complaints.

### 1.3 High-risk domain controls
Agents must not autonomously launch workflows in regulated or high-risk domains without a written control plan. This includes:

- financial trading or investment advice;
- lending, insurance, or underwriting;
- employment screening;
- medical or legal advice;
- surveillance, impersonation, or deceptive persuasion.

---

## 2. Approved Revenue Lanes

Autonomous work should prioritize lanes with clear consent, provenance, and customer value:

1. **First-party inbox-to-CRM operations**
   - Organize client-owned inbound leads.
   - Extract business metadata from messages the client already lawfully received.
   - Draft summaries, tags, follow-ups, and routing suggestions.

2. **Opt-in lead magnets and directories**
   - Build pages, forms, calculators, newsletters, or gated research that collect voluntary signups.
   - Store proof of consent and source of acquisition.

3. **Research products**
   - Produce market maps, benchmarks, reports, templates, or data products from lawful public or licensed sources.

4. **Autonomous listing and commerce services**
   - Create listings, improve sales copy, coordinate permitted marketplace operations, or support seller workflows.

5. **Client-owned workflow automation**
   - Build tools that help a client process its own data under its own policies.

6. **Software and services**
   - Create micro-products, internal tools, automations, and packaged services that solve a business problem without relying on personal-data resale.

---

## 3. RAG and Communications Data Rules

RAG over email or communications content is allowed only when all of the following are true:

- the mailbox owner authorized the workflow;
- the purpose is operational support, analytics, or client benefit rather than data resale;
- retrieval scope is limited to the minimum necessary content;
- outputs do not expose unrelated personal data;
- logs and memory do not persist sensitive content beyond the retention rule.

Additional requirements:

- redact or avoid storing secrets, credentials, and irrelevant personal details;
- prefer extracting business facts, intents, statuses, and action items over raw message bodies;
- do not create datasets for sale from inbox content.

---

## 4. Opportunity Gate

Before activating a revenue lane, score it using `instruments/strategy/score.sh`.

A lane must be rejected if any of the following are true:

- legality is uncertain;
- consent or provenance is weak;
- platform terms are likely violated;
- the workflow depends on selling personal data;
- reserve, risk, or evidence thresholds are not met.

---

## 5. Required Artifacts for Each Program

Each active program must maintain:

- `charter.md` - scope, offer, constraints, and success metrics;
- `journal.md` - ongoing mission diary;
- `improvements.md` - ranked backlog of experiments and fixes.

The strategy intake queue lives in `docs/strategy/incoming.md`.

---

## 6. Execution Principles

1. Prefer durable revenue over fragile hacks.
2. Prefer first-party and opt-in data over third-party personal data.
3. Prefer products and services that improve customer operations.
4. Prefer simulation, paper trading, or sandboxing before live financial exposure.
5. Halt and escalate when legality, consent, or terms are unclear.

---

## 7. Escalation Triggers

Stop the workflow and require sponsor review if any of the following appear:

- requests to scrape or sell personal contacts;
- unclear permission to process communications data;
- requests to impersonate a person or organization;
- requests to evade platform restrictions;
- claims involving guaranteed returns, insider data, or regulatory gray areas.

---

## 8. Canonical Decision

For this repository, the following activities are explicitly disallowed:

- extracting email addresses from Gmail or other files for resale;
- creating or brokering email lists;
- identifying marketplaces or services that buy personal contact data.

The compliant substitute is to build consent-based, first-party, or productized revenue systems instead.
