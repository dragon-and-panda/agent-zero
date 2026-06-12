# Compliance Pack for Autonomous Revenue Programs

This policy bundle governs any Agent Zero workflow that seeks revenue, lead generation, customer acquisition, brokerage, or monetization.

## 1. Non-Negotiable Rules

- Do not scrape, exfiltrate, trade, or sell personal email addresses, phone numbers, inbox contents, or contact lists.
- Do not access private mailboxes, cloud drives, or CRM data unless the data owner has explicitly authorized the workflow for a lawful business purpose.
- Do not design spam systems, unauthorized outreach systems, or gray-market data-brokerage workflows.
- Do not help bypass platform rules, anti-bot protections, or terms of service.
- Do not claim legal compliance unless the workflow has a clear basis for consent, provenance, retention, and permitted use.

## 2. Required Data Controls

Any revenue workflow that touches user or customer data must document:

1. **Source:** where the data came from.
2. **Authority:** why the operator is allowed to use it.
3. **Consent basis:** opt-in, contract, legitimate business record, or other documented lawful basis.
4. **Retention:** how long the data is kept.
5. **Deletion path:** how records are removed on request or policy expiry.
6. **Destination:** where the data is stored and who can access it.

If any of these fields are unknown, the workflow is blocked until clarified.

## 3. Allowed Revenue Lanes

The framework may prioritize:

- First-party workflow automation for a business that already owns the customer relationship.
- Opt-in lead magnets, newsletters, communities, and inbound funnels.
- Productized services where the customer provides their own data and permissions.
- Market research products built from public, licensed, or customer-supplied datasets.
- Listing, merchandising, creative, or operational automation that improves conversion without abusing personal data.
- Internal tooling sold as software, consulting accelerators, or managed workflows.

## 4. Blocked Revenue Lanes

Reject workflows involving:

- Resale of personal contact lists.
- Inbox scraping for third-party lead generation.
- Bulk cold outreach from unverified or non-consensual sources.
- Credential reuse, session hijacking, or mailbox impersonation.
- Unauthorized enrichment of personal profiles from private or semi-private sources.
- Any monetization strategy that depends on deception, regulatory evasion, or platform abuse.

## 5. Evaluation Gates

Before launching a revenue lane, score it against the following:

- **Legality**
- **Consent / provenance clarity**
- **Terms-of-service fit**
- **Operational feasibility**
- **Margin potential**
- **Repeatability**
- **Automation suitability**
- **Reputation risk**

Any lane with failed legality, failed consent, or unknown provenance is automatically rejected regardless of profit potential.

## 6. Preferred Execution Sequence

1. Screen the idea with the revenue-planning tool or scoring instrument.
2. Reject blocked lanes immediately.
3. Convert ambiguous ideas into compliant equivalents.
4. Pilot the lane with synthetic or first-party data.
5. Measure economics before scaling automation.
6. Record outcomes in the mission journal so future runs inherit the decision trail.

## 7. Compliant Reframes for High-Risk Requests

If a user asks for personal-data extraction, list resale, or inbox harvesting:

- Refuse the prohibited part.
- Offer a first-party CRM workflow instead.
- Offer an opt-in acquisition system instead.
- Offer a public-data market research product instead.
- Offer a listing, merchandising, or workflow-automation service instead.

## 8. Documentation Hooks

This file is the canonical policy pack for:

- `docs/programs/agentic_financial_system/charter.md`
- `docs/programs/agentic_financial_system/journal.md`
- `docs/programs/agentic_financial_system/improvements.md`
- `docs/strategy/incoming.md`
- `instruments/strategy/score.sh`
- `python/tools/revenue_planning.py`
