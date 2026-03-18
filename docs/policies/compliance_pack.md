# Compliance Pack for Autonomous Revenue Programs

This policy pack defines the minimum legal, ethical, and operational rules for any monetization workflow run through Agent Zero. It is the canonical reference for the Compliance Guardian described in `docs/autonomous_super_agency.md`.

---

## 1. Core Rule

The system may only pursue revenue through consent-based, lawful, auditable activities that preserve user trust and protect third-party data.

If a workflow depends on deception, private-data resale, spam, account abuse, evasion of platform safeguards, or uncontrolled financial risk, the workflow must be rejected.

---

## 2. Prohibited Activities

The following are always disallowed:

- Harvesting email addresses, contact lists, or inbox metadata without explicit authorization.
- Selling, brokering, renting, or transferring personal email lists or contact databases.
- Using Gmail, Google Workspace, or other inbox data to build outbound lead lists for third parties without documented consent.
- Sending spam, cold outreach at scale without a lawful basis, or attempts to bypass unsubscribe and rate-limit controls.
- Scraping or exporting personal data in ways that violate terms of service, privacy law, or contractual restrictions.
- Buying traffic, reviews, followers, engagement, or marketplace reputation through deceptive means.
- Running financial trading systems with unbounded downside, hidden leverage, or absent written risk controls.
- Routing funds to undocumented personal accounts outside the approved bookkeeping and payout flow.

---

## 3. Required Controls

Every approved workflow must satisfy all of the following:

1. **Consent evidence**
   - The data owner or business principal has granted permission.
   - Purpose of use is documented.
   - Revocation path is defined.

2. **Data minimization**
   - Only the smallest useful subset of data is processed.
   - Sensitive content is excluded unless strictly necessary.
   - Retention windows are defined in advance.

3. **Auditability**
   - Inputs, outputs, decisions, and approvals are logged.
   - Revenue-affecting actions are traceable to an agent, prompt, or instrument.
   - Customer-facing claims can be substantiated.

4. **Platform compliance**
   - Workflows obey API terms, marketplace rules, and content policies.
   - Anti-bot or anti-spam controls are treated as boundaries, not obstacles.

5. **Financial controls**
   - Revenue, refunds, and expenses are recorded in a ledger.
   - Payout destinations are documented and authorized.
   - Speculative capital is ring-fenced from operating cash.

---

## 4. Allowed Revenue Patterns

The following patterns are acceptable when the controls above are met:

- Consent-based inbox-to-CRM cleanup for a business that owns the mailbox.
- Email triage, deduplication, tagging, and analytics for the mailbox owner.
- Opt-in newsletter operations, sponsorship sourcing, and audience analytics.
- Productized research, content operations, and tutorial/course creation.
- Marketplace listing automation for legitimate sellers.
- Affiliate, referral, or software-enabled services with accurate disclosures.
- Backtesting and simulation for trading research; live trading only after separate risk gates are met.

---

## 5. Revenue Safety Gates

Before any revenue program is activated, confirm:

- The offer solves a real problem for a consenting customer.
- The acquisition loop does not rely on personal-data resale.
- There is a refund/remediation path if the output is wrong.
- The workflow can survive a single platform outage or account interruption.
- The downside is bounded and documented.

If any gate fails, the workflow status is `HOLD` or `REJECT`.

---

## 6. Gmail and RAG Policy

RAG over inbox data is allowed only for the mailbox owner or a business that has authorized the workflow. Approved examples:

- Summarizing support requests from the owner's inbox.
- Building a CRM from the owner's own customer conversations.
- Identifying opt-in contacts, existing customers, or partner threads for relationship management.

Disallowed examples:

- Extracting all addresses from received, sent, or CC fields to sell or upload into bulk outreach tools.
- Repurposing private correspondents as leads without permission.
- Building a "bigger list" from unrelated files or inbox history for resale.

---

## 7. Trading and Treasury Policy

Trading is never the first-line monetization engine. It is a downstream capital allocation activity and only becomes eligible when:

- Operating revenue exists from compliant services or products.
- A written risk policy defines max position size, max drawdown, allowed venues, and stop conditions.
- The strategy has been tested in simulation or paper trading.
- Loss of the allocated trading capital does not threaten core operations.

---

## 8. Escalation Rule

When an idea touches personal data, regulated finance, or account-linked automations, the Compliance Guardian must classify it as:

- `GO`: Controls present and risk acceptable.
- `HOLD`: Missing evidence, controls, or documentation.
- `REJECT`: Inherently non-compliant or reputationally unsafe.

Rejected ideas are not "optimized"; they are replaced with adjacent, compliant alternatives.
