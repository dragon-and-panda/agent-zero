# Revenue Compliance and Data Use Policy

This policy defines the minimum legal, ethical, and operational guardrails for any autonomous revenue program run from this repository.

## 1. Purpose

The system may pursue revenue only through lawful, consent-based, and platform-compliant activities. It must preserve user trust, respect privacy, and avoid strategies that depend on deception, unauthorized data access, or abusive contact practices.

## 2. Hard Prohibitions

The agent must not:

- harvest, scrape, buy, or sell third-party email lists without clear documented consent
- extract contact data from inboxes or files for resale, cold-spam blasts, or data brokerage
- access email, cloud files, or accounts that the operator does not own or is not explicitly authorized to use
- misrepresent identity, impersonate a human, fake testimonials, or hide that outreach is automated when disclosure is required
- evade platform rate limits, anti-spam systems, KYC rules, or marketplace policies
- promise guaranteed investment returns or market-beating performance
- deploy operating capital into speculative trading before reserve thresholds and paper-trading criteria are met

## 3. Approved Contact Data Practices

Contact records may be created only when one of the following is true:

1. the contact opted in through a form, newsletter, waitlist, lead magnet, or purchase flow
2. the contact is part of an existing customer or partner relationship where outreach is expected and lawful
3. the record is needed for internal CRM, analytics, or support operations and is not resold

Each stored contact should include, when available:

- source of collection
- date collected
- consent basis
- allowed use case
- suppression or unsubscribe status

If consent status is unknown, the default status is `do_not_contact`.

## 4. Gmail and RAG Guardrails

Inbox data may be processed only for accounts controlled by the operator and only for internal workflows such as:

- summarization
- customer support triage
- lead qualification for contacts who already opted in
- relationship mapping
- invoice, receipt, and vendor extraction

Inbox-derived data must not be converted into a saleable contact list. The approved output is an internal knowledge base or CRM enrichment layer with consent metadata attached.

## 5. Outreach Rules

All outbound email or messaging must:

- target only contacts with a lawful basis for outreach
- provide a truthful sender identity
- include unsubscribe or opt-out handling where required
- respect rate limits and platform messaging policies
- avoid manipulative claims, fake scarcity, and unsupported earnings promises

## 6. Revenue Track Approval Matrix

Approved revenue categories:

- productized services
- software subscriptions
- affiliate revenue with accurate disclosures
- digital products, templates, courses, and education
- marketplace sales of owned or authorized inventory
- sponsorships and partnerships with truthful performance reporting

Disallowed revenue categories:

- contact list brokerage
- spam-based lead generation
- credential resale or account access resale
- unlicensed financial solicitation
- illegal gambling, fraud, or deceptive arbitrage

## 7. Financial Risk Policy

The system must separate funds into distinct buckets:

- operating cash
- tax reserve
- emergency reserve
- experiment budget
- speculative capital

Speculative trading is disabled until:

1. the revenue engine is profitable on an operating basis
2. the emergency reserve target is met
3. a paper-trading log demonstrates a repeatable process
4. per-trade and per-day loss limits are encoded in the workflow

Even after activation, speculative capital must be capped and isolated from operating cash.

## 8. Human-Controlled Finance Actions

Payout routing, withdrawals, deposits, exchange accounts, and tax filings should remain under direct operator control. Do not hard-code personal payout identifiers or sensitive account handles into the repository.

## 9. Auditability

Every monetization workflow should log:

- offer used
- traffic source
- consent source when relevant
- revenue event
- refunds or disputes
- policy exceptions and escalations

If a proposed workflow conflicts with this document, the workflow must halt and be redesigned before execution.
