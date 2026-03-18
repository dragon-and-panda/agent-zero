# Compliance Pack - Ethical Revenue and Data Handling

This policy bundle defines the minimum guardrails for any autonomous revenue workflow built on top of this repository. It is intentionally strict: if a proposed workflow fails these checks, the workflow must stop or be redesigned.

## 1. Non-Negotiable Rules

1. **No personal-data brokerage**
   - Do not harvest, compile, buy, rent, sell, or broker personal email lists, contact databases, or inbox-derived identity graphs.
   - Do not turn received/sent/CC email data into a product for resale.

2. **Consent and lawful basis are mandatory**
   - Only access Gmail, email archives, or related files when the account owner has explicitly authorized that use.
   - Access must be tied to a legitimate first-party business purpose such as search, archiving, CRM cleanup, support retrieval, or relationship management.

3. **No spam or deceptive outreach**
   - Do not automate unsolicited bulk messaging without a documented lawful basis, suppression handling, and platform-policy review.
   - Do not misrepresent identity, affiliation, intent, or sender reputation.

4. **Platform terms matter**
   - Do not build workflows that depend on violating product terms of service, anti-bot controls, or rate-limit protections.
   - If a platform disallows a workflow, that workflow is out of scope until redesigned.

5. **Documented bookkeeping only**
   - Revenue must come from lawful goods or services.
   - Funds movement should only happen into accounts owned or controlled by the operator, with basic bookkeeping records preserved.
   - This repository must not assume ownership of any third-party account or payout destination without separate confirmation outside the codebase.

## 2. Approved Uses of Email + RAG

Email access can support compliant workflows when it stays first-party and consented. Approved examples:

- Searching an owner's inbox for invoices, receipts, support threads, or partner history.
- Building a **private CRM map** for the account owner from their own sent/received mail.
- Deduplicating contacts, tagging relationship context, and preparing opt-in follow-up tasks.
- Creating summaries, retrieval tools, or knowledge packs from a user's own archived correspondence.
- Generating suppression-safe lists such as "do not contact" or "already opted out".

Disallowed examples:

- Selling inbox-derived addresses to marketers, lead brokers, or "traffic" vendors.
- Exporting third-party contact data for unconsented cold outreach.
- Compiling CC/BCC/attachment metadata into tradable lead files.

## 3. Approved Revenue Lanes

The agency may pursue these monetization tracks first:

1. **Inbox-to-CRM Hygiene Service**
   - Convert a consenting client's email history into a private CRM, follow-up queue, and searchable knowledge base.
   - Deliverables: cleaned contact graph, relationship notes, task list, and retention-safe exports.

2. **Autonomous Listing Concierge**
   - Turn seller notes and photos into polished listings, marketplace packages, and buyer-response playbooks.

3. **Public-Web Research Briefs**
   - Sell research packs built from public data, official docs, and client-provided source material.

4. **Process Content / Course**
   - Package the compliant operating system, case studies, and lessons learned into tutorials, playbooks, or media.

## 4. Trading and Capital Allocation Guardrails

- Treat live trading as an advanced phase, not the first source of revenue.
- Start with paper trading and written hypotheses; only consider small live allocations after:
  - stable earned revenue,
  - documented strategy rules,
  - max-loss caps,
  - and post-trade review discipline.
- Never claim guaranteed returns.
- Never use borrowed money, customer funds, or essential operating cash for speculative trades.

## 5. Red Flags That Force a Stop

Immediately reject or pause any workflow that:

- depends on reselling personal email data,
- requires bypassing authorization or platform controls,
- cannot explain its lawful basis in plain language,
- creates outsized reputation risk for short-term gain,
- or moves money without traceable ownership and records.

## 6. Minimum Evidence Checklist

Before a workflow goes live, capture:

- purpose statement,
- data sources used,
- consent and ownership status,
- platform-policy check,
- expected revenue path,
- downside / failure modes,
- and kill-switch conditions.

If any item is missing, the workflow remains in draft status.
