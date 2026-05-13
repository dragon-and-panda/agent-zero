# Agentic Financial System Charter

## Mission

Build a self-sustaining financial system through legal, ethical, low-touch online ventures that can be operated and improved by Agent Zero with minimal supervision.

## Non-Goals

- No personal-email harvesting
- No contact-list brokerage
- No spam or bulk cold outreach without consent
- No unauthorized access to Gmail or other private systems
- No revenue strategy that depends on privacy abuse or platform evasion

## Approved Operating Principle

Whenever a task mentions Gmail, email archives, or file-based contact data, the allowed use is first-party retrieval and workflow support only. The disallowed use is extracting or reselling email addresses.

## Current Revenue Lanes

### 1. Inbox-to-CRM Assistant
- Use case: retrieve context from the user's own inbox, summarize threads, tag intent, and draft follow-ups for existing or opted-in contacts.
- Monetization path: internal productivity gains, agency services, or a productized assistant.
- Guardrail: never export private inbox contacts into a resale or brokerage flow.

### 2. Autonomous Listing Service
- Use case: improve listings, descriptions, pricing hypotheses, and operational workflows for marketplace inventory.
- Monetization path: service retainers or performance-linked operations.
- Reference: `docs/autonomous_listing_service.md`

### 3. Research Brief and Lead-Magnet Pipeline
- Use case: publish niche intelligence reports, templates, calculators, or benchmark packs.
- Monetization path: paid reports, subscriptions, or inbound lead capture with explicit opt-in.

### 4. Workflow Automation Retainers
- Use case: build compliant internal automations for small businesses, including triage, CRM hygiene, reporting, and support workflows.
- Monetization path: setup fees, retainers, or usage-based contracts.

## Operating Loop

1. Add candidate venture to `docs/strategy/incoming.md`
2. Score it with `instruments/strategy/score.sh`
3. Reject or redesign anything that fails legality, consent, provenance, or platform checks
4. Build the smallest revenue-bearing version
5. Measure margin, repeatability, automation depth, and defensibility
6. Reinvest into the highest-signal lane

## Tooling Notes

- RAG over Gmail is only acceptable for first-party retrieval, summarization, and CRM support.
- Orange DataScaping or similar analysis tools may only be used on consented, first-party, or clearly public-business datasets.
- Any future outreach system must rely on explicit opt-in or pre-existing lawful relationship context.
