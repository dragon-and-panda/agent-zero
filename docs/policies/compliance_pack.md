# Compliance Pack for Autonomous Revenue Programs

This policy pack defines the minimum operating rules for any autonomous workflow in this repository that touches revenue generation, customer data, outreach, marketplaces, or capital allocation.

The goal is simple: maximize lawful, ethical, repeatable revenue while protecting user privacy, platform trust, and downside exposure.

---

## 1. Non-Negotiable Rules

1. **Authorized data only**
   - Process only data the operator owns or is explicitly authorized to access.
   - Any Gmail or inbox retrieval workflow must be limited to user-controlled accounts and documented business purposes.

2. **No sale or transfer of harvested contact data**
   - Do not compile, broker, rent, or sell email lists gathered from personal inboxes, scraped sources, or third-party systems.
   - Extracted contacts may be used only for first-party CRM, supplier management, support history, or consent-based segmentation.

3. **Consent-based outreach only**
   - Marketing systems must target opted-in subscribers, existing customers, warm referrals, or lawful B2B contacts where the operator has a compliant basis for contact.
   - Every outreach workflow must support unsubscribe handling and suppression lists.

4. **No deceptive automation**
   - Do not impersonate humans, fake testimonials, create false scarcity, conceal affiliate relationships, or misrepresent inventory, pricing, or performance.

5. **Platform and terms compliance**
   - Marketplace, email, and payment workflows must respect rate limits, anti-spam rules, content policies, and disclosure requirements.
   - If a platform forbids a workflow, the workflow is disallowed even if it is technically possible.

6. **Capital preservation before speculation**
   - Do not deploy automated live trading until the strategy has passed paper-trading and controlled-risk gates.
   - No promises of returns, no reckless leverage, and no autonomous capital allocation without documented limits.

7. **Auditability**
   - Every monetization experiment must document: objective, data source, legal basis, expected downside, stop conditions, and results.

---

## 2. Approved Revenue Modes

The following models fit the intended direction of this repository and may be automated further:

- Marketplace listing optimization and syndication for operator-owned or client-owned inventory
- Productized services built on top of the autonomous listing service
- Opt-in newsletters and audience-building funnels
- Affiliate content with clear disclosures
- Digital products, tutorials, templates, and courses
- Client-authorized CRM cleanup, inbox triage, and contact deduplication
- Supplier research, lawful sourcing, and first-party catalog expansion

---

## 3. Restricted or Escalation-Only Modes

These areas require extra controls, phased rollout, and explicit documentation:

- Gmail or inbox RAG tied to personal communications
- Browser automation against websites with anti-bot or rate-limit sensitivity
- Any workflow storing personal data outside the primary runtime
- Payments, refunds, or account movement actions
- Trading, speculative strategies, or capital deployment

For these categories, the workflow must include a dry-run or simulation mode, explicit fallback handling, and a documented human review point before production use.

---

## 4. Required Checks Before Launch

Before a new revenue workflow goes live, the owning agent must:

1. Score the opportunity with `instruments/strategy/score.sh`.
2. Record the operating model in `docs/programs/<program>/journal.md`.
3. Confirm the data source is authorized and purpose-limited.
4. Define reserve thresholds, rollback steps, and stop-loss conditions.
5. Verify that logs do not expose unnecessary personal data.

---

## 5. Contact Data Handling Standard

If inbox or CRM data is involved:

- Store only the minimum fields needed for the workflow.
- Default use cases:
  - customer support continuity
  - supplier or buyer relationship tracking
  - segmentation of opted-in contacts
  - deduplication and enrichment of first-party CRM records
- Prohibited use cases:
  - resale of contact lists
  - mass cold outreach to scraped or non-consenting contacts
  - transfer of inbox-derived personal data to unrelated third parties

---

## 6. Capital Allocation Gate

Any move from cash generation into trading or similar strategies must follow this sequence:

1. Build cash reserves from lower-risk revenue streams.
2. Define maximum loss, position sizing, and daily stop rules.
3. Run paper-trading with logged metrics.
4. Review win rate, expectancy, drawdown, and operational reliability.
5. Start with constrained live exposure only after the prior gates pass.

Until those gates are complete, research and simulation are allowed; autonomous live trading is not.

---

## 7. Default Kill Switches

Pause the workflow immediately if any of the following occurs:

- A data source appears unauthorized or over-collected
- A platform warns, rate-limits, or suspends an account
- Refunds, disputes, or complaint rates rise above the documented threshold
- A live strategy breaches its drawdown or reserve limit
- Logs show policy drift or undisclosed behavior

This pack should be linked from program charters and referenced by any agent tasked with monetization or growth.
