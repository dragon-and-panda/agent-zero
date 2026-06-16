# Strategy Intake Queue

Use this file as the top-level intake queue for new autonomous missions before they are turned into program blueprints, instruments, or prompt changes.

Each entry should be concise, testable, and compliant with `docs/policies/compliance_pack.md`.

---

## Intake Template

```md
### Mission
- Name:
- Sponsor intent:
- Primary customer:
- Problem to solve:
- Proposed offer:
- Why now:

### Revenue Thesis
- How money is earned:
- First transaction path:
- Recurring or repeatable component:
- Constraints:

### Data and Tooling
- Owned data sources:
- Consented data sources:
- External tools and platforms:
- RAG or analytics need:

### Guardrails
- Privacy risks:
- Compliance considerations:
- Explicitly forbidden tactics:

### Success Metrics
- Leading indicators:
- Revenue indicators:
- Quality indicators:
```

---

## Seed Mission: Ethical Financial System

### Mission
- Name: Ethical Financial System
- Sponsor intent: build a self-sustaining, low-touch revenue engine using Agent Zero
- Primary customer: small businesses, creators, and sellers who need AI-assisted operations
- Problem to solve: operators have underused inbox knowledge, fragmented workflows, and inconsistent follow-up
- Proposed offer: combine inbox intelligence, CRM hygiene, content generation, and productized automation into repeatable services and software
- Why now: the repo already contains autonomy, memory, and knowledge primitives that can be assembled into a revenue OS

### Revenue Thesis
- How money is earned: subscriptions, service retainers, marketplace fees, or packaged automation projects
- First transaction path: sell a narrowly scoped service built from owned or consented data
- Recurring or repeatable component: recurring reporting, follow-up automation, listing management, or knowledge retrieval
- Constraints: no selling personal data, no unauthorized inbox access, no spam workflows

### Data and Tooling
- Owned data sources: operator Gmail/Workspace, proposals, support history, product docs, internal notes
- Consented data sources: CRM exports, form submissions, newsletter opt-ins
- External tools and platforms: Gmail exports/APIs, Orange DataScaping, CRM, marketplaces, billing stack
- RAG or analytics need: identify FAQs, recurring pain points, missed opportunities, high-intent prospects, and reusable sales assets

### Guardrails
- Privacy risks: private correspondence, secrets in email, mixed personal/business data
- Compliance considerations: anti-spam, consent logging, deletion handling, platform terms
- Explicitly forbidden tactics: email-list brokerage, scraping private addresses, unsolicited mass outreach from harvested data

### Success Metrics
- Leading indicators: qualified conversations, recovered opportunities, response-time reduction, repeatable workflow count
- Revenue indicators: first sale, monthly recurring revenue, gross margin, payback period
- Quality indicators: opt-out rate, complaint rate, data provenance coverage, manual escalations
