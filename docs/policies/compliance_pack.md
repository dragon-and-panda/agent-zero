# Compliance Pack for Autonomous Revenue Programs

This pack defines the non-negotiable guardrails for any monetization workflow built or operated with Agent Zero.

## 1. Hard Prohibitions

The system must not:

- scrape, extract, broker, resell, or "monetize" personal email addresses or contact lists;
- access inboxes, cloud drives, or private accounts without explicit, revocable authorization from the account owner;
- send spam, evade platform rate limits, bypass anti-abuse controls, or disguise automation as a human;
- process personal data outside the narrow, disclosed purpose for which it was provided;
- misrepresent affiliations, impersonate people, or falsify listings, reviews, testimonials, or business records;
- enter regulated financial, legal, medical, or identity workflows without the controls required for that domain.

Any request that depends on those behaviors must be rejected or converted into a compliant alternative.

## 2. Required Gates Before Execution

Every new revenue lane must be screened for:

1. legality;
2. consent;
3. data provenance;
4. platform-rule alignment;
5. operational reversibility.

If legality, consent, provenance, or platform alignment is unclear, the lane stays on HOLD. If any of those are clearly weak, the lane is REJECTED.

## 3. Approved Data Handling Patterns

Allowed patterns include:

- user-owned data connected with explicit permission;
- first-party CRM/contact data collected through clear opt-in flows;
- public business information used within the source platform's terms;
- synthetic or self-generated data for testing and benchmarking;
- aggregated, anonymized reporting where re-identification risk is materially reduced.

## 4. Preferred Revenue Lanes

Priority should go to automation that creates value without exploiting private data:

- inbox-to-CRM organization for the account owner;
- autonomous listing and marketplace operations for a consenting seller;
- research products, dashboards, and alerts based on lawful sources;
- lead magnets, newsletters, and outbound systems that only use opted-in audiences;
- software, services, and digital products with clear customer benefit.

## 5. Execution Controls

- Use the strategy scoring instrument before starting a new lane.
- Keep a journal entry for each material decision.
- Favor pilots that are reversible, low-cost, and easy to audit.
- Store only the minimum data needed for the job.
- Prefer official APIs and documented integrations over scraping or brittle browser automation.

## 6. Escalation Rule

If a workflow appears profitable but depends on privacy invasion, personal-data resale, or platform abuse, stop and redesign the workflow instead of trying to optimize it.
