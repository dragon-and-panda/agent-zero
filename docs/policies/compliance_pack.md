# Compliance Pack: Agentic Financial System

This policy pack governs any autonomous revenue program built in this repository.

## 1. Core rule set

- Operate only through ethical and lawful means.
- Do not collect, sell, rent, trade, or disclose personal data without a valid legal basis and explicit authorization.
- Do not use spam, deceptive messaging, account takeovers, credential abuse, or terms-of-service evasion.
- Do not build workflows whose primary value depends on privacy invasion, unauthorized scraping, or non-consensual outreach.
- Prefer durable, service-based, or product-based revenue over speculative gain.

## 2. Email and inbox data policy

Email-derived data is allowed only for sponsor-owned or explicitly authorized workflows such as:

- inbox cleanup and CRM hygiene for the mailbox owner,
- support triage and routing,
- invoice and sales pipeline organization,
- extraction of opted-in contacts into a sponsor-controlled CRM,
- internal analytics for response times, funnel stages, or customer support quality.

Email-derived data is not allowed for:

- compiling contact lists for resale or brokerage,
- cold outreach to people who did not opt in,
- extracting contacts from received, sent, CC, or archived mail for third-party monetization,
- bypassing provider controls, retention rules, or consent boundaries,
- repurposing private correspondence into a lead database.

## 3. Approved data acquisition patterns

Use only one or more of the following:

1. Sponsor-owned datasets.
2. Explicitly opt-in leads.
3. Public business information where collection and use are permitted.
4. First-party interactions where the user is informed and the workflow is documented.

Each workflow should record:

- data source,
- legal basis or consent basis,
- retention period,
- deletion path,
- downstream systems that receive the data.

## 4. Revenue model classification

### GO

- Consent-based inbox-to-CRM hygiene service.
- Autonomous listing optimization and resale operations.
- AI operations consulting for small businesses.
- Documentation products, playbooks, and courses built from owned work.
- Affiliate or referral programs using consented audiences and clear disclosures.

### HOLD

- Any workflow involving regulated financial advice, payments handling, or brokerage.
- Trading systems beyond paper trading.
- High-volume outreach systems that need compliance review for local anti-spam law.

### REJECT

- Personal email list brokerage.
- Inbox harvesting for lead resale.
- Non-consensual lead generation from private communications.
- Mass messaging systems designed to evade rate limits or platform policy.
- Unlicensed investment solicitation or funds handling on behalf of others.

## 5. Trading and treasury controls

Speculative trading, including Forex, is disabled by default.

It remains in HOLD status until all of the following are true:

1. An operating reserve exists that covers the core business runway.
2. A written risk policy defines allowed instruments, max daily loss, max drawdown, and stop conditions.
3. A paper-trading track record exists over a meaningful sample size.
4. Jurisdiction, tax, and platform compliance has been reviewed.
5. Trading capital is ring-fenced from operating cash.

Directing funds to arbitrary third-party payment handles is not an automated action in this framework. Treasury movement should occur only through sponsor-controlled, documented accounts and approved bookkeeping flows.

## 6. Required safeguards for autonomous programs

- Diversify revenue across at least two independent tracks before scaling spend.
- Keep human-readable SOPs in `docs/programs/`.
- Log decision rationale, risk notes, and next actions in a mission journal.
- Build kill switches for any automation that contacts users, moves money, or touches sensitive data.
- Prefer reversible experiments before irreversible commitments.

## 7. Escalation conditions

Pause the workflow and escalate if any of the following occur:

- consent status is unknown,
- a platform policy clearly forbids the workflow,
- a payment or finance flow would handle another party's funds,
- sensitive data would be exported outside the approved system boundary,
- the only path to monetization depends on resale of personal data.
