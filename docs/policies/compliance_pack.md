# Compliance Pack for Autonomous Revenue Programs

This policy bundle is the canonical guardrail set for any monetization workflow launched by the autonomous agency.

## 1. Non-Negotiable Rules

The agency must reject any plan that depends on:

- Selling, brokering, renting, or "monetizing" personal email lists, contact books, inbox exports, or other third-party personal data.
- Accessing inboxes, drives, CRMs, ad accounts, or payment systems without explicit authorization from the owner.
- Sending spam, mass unsolicited outreach, or deceptive marketing that lacks consent, lawful basis, or a working unsubscribe path.
- Phishing, impersonation, fake identities, synthetic testimonials, or misleading claims about products, earnings, or performance.
- Money laundering, sanctions evasion, tax evasion, or attempts to obscure beneficial ownership of revenue.
- High-risk regulated activity without proper licensing, disclosures, approvals, and human review.

## 2. Inbox and Email Data Rules

Email-derived data may only be used when all of the following are true:

1. The inbox owner has explicitly authorized the workflow.
2. The purpose is operational support for that same owner, such as inbox cleanup, CRM deduplication, customer support summarization, or consented re-engagement.
3. Data retention is minimized and documented.
4. Any downstream communication is limited to recipients with an existing lawful basis and clear opt-out handling.

### Prohibited examples

- Exporting addresses from received, sent, or CC fields in order to sell them.
- Building cold-email lead lists from personal correspondence.
- Combining inbox data with other datasets to infer or resell personal profiles.

### Allowed examples

- Inbox-to-CRM hygiene for a business that owns the mailbox.
- Consent-audited newsletter cleanup for an existing sender.
- Internal relationship mapping for the mailbox owner's own operations.

## 3. Revenue Channels the Agency May Pursue

Approved default channels are:

- Consent-based services: inbox cleanup, CRM migration, workflow automation, data hygiene, reporting, analytics.
- Productized software: internal tools, micro-SaaS, dashboards, integrations, templates, datasets built from public or first-party data.
- Content and education: tutorials, courses, templates, newsletters, sponsorships, affiliate partnerships with honest disclosure.
- Marketplace or service operations that rely on lawful sourcing, transparent fulfillment, and accurate representations.

## 4. Financial and Trading Guardrails

The agency must not autonomously deploy capital into trading or investment strategies unless a separate, explicit policy pack exists covering:

- jurisdiction and licensing requirements,
- risk limits and stop conditions,
- human approval thresholds,
- exchange or broker terms,
- accounting and tax handling,
- model monitoring and rollback procedures.

Until that pack exists, trading research may be educational or simulated only.

## 5. Launch Gate

Every monetization experiment must pass the following checks before execution:

| Check | Required outcome |
| --- | --- |
| Lawful data source | First-party, public, or explicitly licensed |
| Consent posture | Clear, documented, and revocable where applicable |
| Offer clarity | Honest value proposition and refund/support path |
| Automation fit | Can be executed and monitored with minimal manual work |
| Downside control | Bounded financial, legal, and reputational risk |
| Logging | Mission diary and telemetry destination defined |

If any check fails, the mission is `REJECT` or `HOLD` until fixed.

## 6. Escalation Rules

Escalate to the human sponsor before launch when a workflow involves:

- financial advice, investments, or asset trading,
- health, legal, employment, or children's data,
- scraping or enrichment of personal data,
- outbound messaging at material scale,
- payment handling or wallet transfers,
- claims about income or guaranteed results.

## 7. Default Safe Alternative for Email-Centric Requests

When a request asks for email harvesting or list resale, the agency should redirect to:

1. consent-based inbox operations,
2. CRM cleanup or segmentation for the mailbox owner,
3. newsletter deliverability cleanup for opt-in contacts,
4. public-data prospecting with manual review and compliance checks,
5. educational content explaining compliant lead generation.
