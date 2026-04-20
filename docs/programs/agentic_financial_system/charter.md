# Agentic Financial System Charter

## Mission

Build a self-sustaining financial system through lawful, ethical, low-touch online ventures that compound over time.

## Non-negotiables

- follow `docs/policies/compliance_pack.md`
- do not harvest or sell personal email lists
- do not convert inboxes or exported mail into resale datasets
- do not rely on spam, deception, or unauthorized access
- prefer first-party, opt-in, customer-owned workflows

## Operating model

The system should combine several revenue lanes so it does not depend on a single fragile channel:

1. inbox-to-CRM operations for customer-owned mailboxes
2. autonomous listing and marketplace operations
3. research products and briefs built from aggregate or user-supplied data
4. implementation services for compliant automation, RAG, and workflow tooling

## Data policy for email and RAG

Email data may only be processed when:

- the mailbox owner or authorized admin requested the work
- the purpose is internal assistance, triage, CRM extraction, search, or drafting
- the data stays inside the customer workflow
- downstream contact use remains permissioned and first-party

Orange DataScaping or similar analysis tools may be used only on authorized, permissioned datasets for clustering, prioritization, or reporting. They must not be used to organize harvested personal-contact inventories for sale.

## Lane design criteria

Every lane should aim for:

- repeatable demand
- strong automation fit
- acceptable margins
- low platform and compliance risk
- evidence that value is created without exploiting people or data

## Activation gate

Before a lane is activated:

1. log it in `docs/strategy/incoming.md`
2. score it with `instruments/strategy/score.sh`
3. reject, hold, or pass it based on legality, consent, provenance, platform risk, and execution quality
4. write updates to `docs/programs/agentic_financial_system/journal.md`

## Initial portfolio

### Lane A: compliant inbox-to-CRM service

- input: customer-owned mailbox access with written authorization
- output: structured contacts, opportunities, summaries, and draft replies inside the customer's systems
- monetization: setup fee plus recurring operations retainer

### Lane B: autonomous listing service

- input: product or property information from the owner
- output: enriched descriptions, publishing workflows, and marketplace operations
- monetization: service fee, success fee, or managed listing subscription

### Lane C: research and workflow products

- input: public aggregate data or user-provided data
- output: paid briefs, dashboards, templates, and decision support
- monetization: subscriptions, custom reports, or packaged internal tools

## Current priority

Prioritize Lane A first because it can reuse existing RAG and workflow capabilities without violating privacy rules, while Lanes B and C provide diversification.
