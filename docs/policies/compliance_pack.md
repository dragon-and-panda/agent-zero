# Compliance Pack for Autonomous Revenue Programs

This pack defines the minimum legal, privacy, and platform-safety rules for any
Agent Zero workflow that touches monetization, personal data, outreach, or
third-party platforms.

## Non-negotiable prohibitions

The agent must not design, automate, or optimize any workflow that depends on:

- harvesting personal email addresses or contact details without consent
- brokering, renting, or selling personal email lists or contact lists
- scraping inboxes, Gmail, or other mail systems without explicit authorization
- spam, deceptive outreach, impersonation, or undisclosed bulk messaging
- bypassing website terms of service, robots rules, rate limits, or access rules
- credential abuse, session theft, account takeover, or privacy circumvention
- laundering unclear data provenance through "research" or "enrichment" labels

If a requested mission depends on any of the above, the correct outcome is
`REJECT` plus a compliant alternative.

## Allowed classes of revenue work

The agent may help with monetization when the workflow is lawful, documented,
and based on consent or legitimate first-party operations, including:

- opt-in lead generation, newsletters, and waitlists
- first-party CRM hygiene, segmentation, and follow-up drafting
- user-owned inbox triage for support, sales, or partnership operations
- public market research, benchmarking, and productized reports
- listing, marketplace, and directory services built from lawful sources
- content, affiliate, education, and service businesses

## Rules for email and messaging data

Email-related automation is allowed only when all of the following are true:

1. The mailbox owner has explicitly authorized access.
2. The purpose is operational work for that owner, not resale.
3. Retained data is minimized to what the task requires.
4. Sensitive personal data is not exposed in outputs unless necessary.
5. Outreach uses permission-based contacts or existing lawful relationships.

RAG over email may be used for summarization, triage, CRM sync, and internal
analytics on authorized mailboxes. It must not be used to create resaleable
contact databases or spam targets.

## Required launch gates

Before activating any revenue lane, verify:

- legality: the workflow is lawful in the relevant jurisdiction
- consent: personal data use is authorized and purpose-limited
- provenance: data sources are documented and auditable
- platform fit: the workflow complies with product and marketplace terms
- reversibility: the agent can stop or roll back without harming users

If any hard gate fails, the lane is `REJECT`.

## Preferred compliant substitutes

When a user asks for contact harvesting or list resale, redirect to one or more
of these patterns instead:

1. Build an opt-in acquisition funnel with landing pages, lead magnets, and CRM
   tagging.
2. Build an inbox-to-CRM assistant for a user-owned mailbox with audit logs.
3. Build public-source research products, benchmarks, or directories.
4. Build listing-management or marketplace operations for client-owned assets.

## Execution checklist

For each active revenue workflow, keep:

- a plain-language mission brief
- data-source provenance notes
- a score from `instruments/strategy/score.sh`
- stop conditions and human escalation triggers
- a journal entry in `docs/programs/agentic_financial_system/journal.md`

## Escalation rule

If the legality, privacy basis, or platform compliance of a workflow is unclear,
hold the lane, document the uncertainty, and propose a lower-risk alternative
instead of acting.
