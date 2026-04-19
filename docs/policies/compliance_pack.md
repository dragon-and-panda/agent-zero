# Compliance Pack

This repository may be used to automate research, outreach, listings, and revenue experiments. Those workflows must remain legal, ethical, consent-based, and compatible with platform rules.

## Non-negotiable prohibitions

Do not build or run systems that:

- extract personal email addresses or contact lists for resale
- scrape inboxes, mailboxes, or accounts without the account owner's explicit authorization
- send spam or bulk outreach to people who did not opt in
- broker, enrich, or trade third-party personal data with unclear provenance
- bypass rate limits, CAPTCHAs, anti-bot controls, or platform terms of service
- access credentials, sessions, or private content that the operator does not lawfully control

## Allowed patterns

The following lanes are acceptable when they are backed by documented consent and lawful access:

- first-party inbox triage, summarization, and CRM sync for a user-owned mailbox
- opt-in newsletter, waitlist, or lead magnet funnels
- customer support and sales operations for a client-owned CRM
- marketplace listing creation and management for goods the seller controls
- anonymized or aggregate research products that do not expose personal data
- internal analytics on user-supplied datasets with documented provenance

## Rules for Gmail, RAG, and data extraction

If Gmail or other email data is used with RAG:

1. the mailbox must be owned by the operator or a client that granted explicit permission
2. the purpose must be operational for that owner, such as search, summarization, routing, or CRM updates
3. extracted data must stay inside that owner's workflow unless explicit consent covers another use
4. contact information must not be compiled for sale, rental, or non-consensual outreach

If Orange Data Mining or similar tooling is used, feed it only data that passes the same legality, consent, provenance, and platform-rule checks.

## Decision gates before activation

Every revenue lane must clear these gates before implementation:

1. legality
2. consent
3. data provenance
4. platform and contract terms
5. operational reversibility
6. reserve and downside controls

If legality, consent, provenance, or platform compliance is weak, the lane must be rejected or reframed before any buildout continues.

## Preferred compliant substitutes

When a request asks for inbox scraping, contact-list extraction, or list resale, reframe into one of these:

- inbox-to-CRM automation for opted-in contacts
- first-party lead capture assets and landing pages
- listing arbitrage or autonomous resale services using lawful seller inventory
- agentic research subscriptions based on public or licensed data
- workflow automation services sold to businesses that own their data
