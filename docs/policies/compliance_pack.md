# Compliance Pack for Autonomous Revenue Programs

This document is the canonical policy bundle for any Agent Zero workflow that touches monetization, communications, personal data, financial accounts, or trading systems.

---

## 1. Non-Negotiable Rules

1. **No personal-data brokering**
   - Do not scrape, compile, buy, sell, rent, or trade email lists or other personal contact data.
   - Do not extract contacts from inboxes, sent mail, cc fields, or files for resale, spam, or undisclosed outreach.
2. **Consent first**
   - Contact data may only be processed when the data subject or account owner has authorized the use case.
   - Approved uses include personal CRM cleanup, first-party newsletter management, customer support, and client-owned outreach with lawful consent records.
3. **No deceptive acquisition**
   - Do not impersonate people, businesses, or platforms.
   - Do not use fake identities, fabricated testimonials, or misleading landing pages to collect leads or payments.
4. **No unlawful platform abuse**
   - Respect site terms, robots rules, API policies, anti-spam laws, and data protection obligations.
   - Avoid credential harvesting, CAPTCHA circumvention for unauthorized access, or evasion of platform safety controls.
5. **No uncontrolled financial risk**
   - Live trading is prohibited until simulation metrics, reserve thresholds, and risk controls pass documented gates.
   - No leverage escalation, martingale behavior, or hidden exposure.
6. **Auditability required**
   - Every revenue program must log decisions, assumptions, failures, and policy checks in a mission diary.

---

## 2. Allowed Monetization Lanes

The framework should prioritize businesses with explicit customer value, repeatability, and low regulatory risk:

- **Opt-in lead generation:** landing pages, directories, waitlists, and newsletters where subscribers knowingly provide their information.
- **Client-owned CRM enrichment:** deduplication, segmentation, tagging, and workflow automation for contact lists the client lawfully owns.
- **Service businesses:** listing optimization, research support, analytics setup, automation implementation, content repurposing, or reporting.
- **Digital products:** templates, prompt packs, guides, courses, calculators, dashboards, and niche knowledge products.
- **Affiliate and referral programs:** only with accurate disclosures and truthful claims.
- **Software or data products:** analytics, monitoring, summarization, or workflow tools built on first-party or licensed data.
- **Marketplace operations:** compliant listing creation, pricing support, negotiation support, and fulfillment automation.

---

## 3. Restricted / Disallowed Mission Patterns

The following mission patterns are out of scope and must be replaced with compliant alternatives:

| Disallowed Pattern | Why It Fails | Compliant Replacement |
| --- | --- | --- |
| Selling harvested email lists | Privacy invasion, spam risk, likely unlawful | Build opt-in audiences and sell services/products to them |
| Mining Gmail contacts for resale | No consent, account abuse risk | Use inbox data only for owner-authorized analytics or CRM hygiene |
| Buying traffic with deceptive promises | Consumer protection risk | Use clear offers, disclosures, and verifiable value |
| Immediate live forex trading with untested strategy | High loss/regulatory risk | Run paper trading, then controlled pilots with hard limits |

---

## 4. Required Program Gates

No mission moves forward unless all required gates are satisfied.

### Gate A: Legality and Consent
- Document the data source and why its use is lawful.
- Record whether each workflow touches personal data.
- If consent is absent or unclear, stop and redesign the workflow.

### Gate B: Unit Economics
- The offer must identify:
  - target customer,
  - value delivered,
  - acquisition channel,
  - expected cost to deliver,
  - fallback if conversion is weak.

### Gate C: Automation Safety
- Define rate limits, budget caps, and a kill switch.
- Log all outbound messaging drafts before sending.
- Require human or policy approval for edge cases.

### Gate D: Financial Risk
- Before live capital deployment, require:
  - paper-trading history,
  - maximum drawdown limit,
  - stop-loss rules,
  - reserve capital separate from operating cash.

---

## 5. Gmail / Email Data Policy

RAG over email can be allowed only for the mailbox owner's internal productivity use cases, such as:
- summarizing threads,
- extracting tasks,
- finding prior conversations,
- organizing an owned CRM,
- identifying opt-in prospects already in a lawful sales pipeline.

RAG over email is **not** allowed for:
- contact harvesting,
- data resale,
- list brokering,
- spam campaigns,
- inferring sensitive personal traits for monetization.

If email data is used at all:
- minimize fields retained,
- prefer aggregation over raw exports,
- redact secrets and unrelated personal data,
- keep access scoped to the account owner or an authorized client account.

---

## 6. Trading Policy

Trading is a late-stage program, not the first revenue engine.

1. Start with **simulation only**.
2. Promote to a tiny live pilot only after documented positive expectancy, controlled drawdown, and operational reserves are in place.
3. Use diversified, rules-based risk controls:
   - fixed position sizing,
   - per-trade stop-loss,
   - daily loss cap,
   - weekly review and shutdown criteria.
4. Never rely on trading proceeds to fund core operating expenses.

---

## 7. Cash Handling and Financial Controls

- Separate operating cash, reserves, taxes, and experimental capital.
- Reconcile revenue by channel.
- Keep evidence of invoices, payouts, fees, and refunds.
- Do not route funds through opaque or misleading payment flows.
- Any payout destination must be configured only after verifying ownership and compliance obligations.

---

## 8. Redundancy and Contingency Standards

Every program needs:

- **Primary lane:** the current best revenue engine.
- **Secondary lane:** a different channel or offer that can absorb demand shocks.
- **Reserve buffer:** cash reserved for refunds, chargebacks, or failed experiments.
- **Rollback plan:** steps to pause campaigns, disable automations, and notify affected parties.
- **Dependency map:** note single points of failure such as one platform, one payment rail, or one supplier.

---

## 9. Default Escalation Rule

If a requested workflow depends on privacy invasion, deception, or unclear legality, the agent must decline that path and convert the mission into a lawful equivalent with documented alternatives.
