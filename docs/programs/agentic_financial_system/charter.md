# Agentic Financial System Charter

## Mission

Build a self-sustaining financial system through lawful, ethical, repeatable online ventures that can be operated with high autonomy and low human touch.

## Non-negotiable constraints

- no personal-data resale
- no inbox scraping without explicit owner authorization
- no spam, phishing, or deceptive acquisition
- no platform-rule evasion
- no monetization lane with unclear legality, consent, or provenance

## Approved venture lanes

### Lane 1: First-party inbox-to-CRM hygiene
- Input: owner-authorized mailbox exports, support archives, customer CSVs
- Output: deduplicated contacts, tags, summaries, and CRM-ready enrichment
- Revenue model: done-for-you service, retainer, or internal efficiency gain
- Guardrail: contacts remain with the data owner and are never sold

### Lane 2: Autonomous listing and merchandising services
- Input: product photos, catalog data, listing requirements
- Output: descriptions, image improvements, publication workflows
- Revenue model: service fees, managed operations, or software subscription
- Repo anchor: `docs/autonomous_listing_service.md`

### Lane 3: Public-data research products
- Input: public websites, filings, vendor pages, market documentation
- Output: market maps, vendor directories, briefs, and competitive intelligence
- Revenue model: report sales, subscriptions, or consulting
- Guardrail: use lawful public sources and cite provenance

### Lane 4: Opt-in audience growth
- Input: first-party content, lead magnets, consented signups
- Output: newsletter funnels, landing pages, educational assets, lifecycle sequences
- Revenue model: affiliate income, sponsorships, consulting upsells, or owned products
- Guardrail: every outreach list must be permission-based

## Activation checklist

Before a lane goes live:

1. Score it with `instruments/strategy/score.sh`.
2. Confirm legality, consent, provenance, and platform-fit are high confidence.
3. Write the lane definition and current hypothesis into `docs/strategy/incoming.md`.
4. Reject or redesign any tactic that depends on private-data brokerage.

## What this mission is not

This mission does not include selling compiled email lists, brokering private contact data, or turning inbox content into third-party lead inventory. If a prompt asks for that, the system must redirect to a compliant first-party or public-data lane.
