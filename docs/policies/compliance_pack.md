# Compliance Pack for Autonomous Revenue Workflows

This pack defines the minimum guardrails for any workflow that attempts to make money, handle customer data, or automate outreach.

## Core rule

Revenue must come from lawful, ethical products or services. The system must not monetize by harvesting, brokering, exposing, or reselling personal data.

## Hard prohibitions

- Do not scrape, compile, buy, rent, broker, or sell personal email lists or contact databases.
- Do not access Gmail, Google Workspace, inboxes, or files unless the mailbox owner or authorized client explicitly granted access for a legitimate business purpose.
- Do not turn inbox data into a resale asset. Authorized inbox access is for internal workflow automation, CRM hygiene, support operations, or analytics only.
- Do not bypass authentication, rate limits, CAPTCHAs, paywalls, or platform terms of service.
- Do not send spam, deceptive outreach, or impersonated messages.
- Do not combine first-party data with scraped third-party personal data to create lead lists.

## Allowed monetization lanes

- Sell software, services, templates, automations, or managed operations.
- Use first-party, opt-in, or client-authorized data to improve internal workflows.
- Build research products from public, licensed, aggregated, or de-identified data.
- Run listing and marketplace operations for lawful goods or services.
- Grow an opt-in audience through newsletters, lead magnets, communities, or content products.

## Data handling rules

Before using any dataset, answer all of the following with a clear yes:

1. Is the data source authorized?
2. Is the provenance documented?
3. Is the intended use compatible with consent and platform terms?
4. Is the workflow avoiding unnecessary personal data exposure?
5. Can the decision and data path be audited later?

If any answer is no or unknown, the lane is not ready for execution.

## Gmail and RAG specific guidance

- RAG over Gmail or Google Workspace data is allowed only for the mailbox owner or an explicitly authorized client account.
- Valid uses include inbox triage, CRM updates, follow-up drafting, support summarization, and relationship intelligence for internal use.
- Invalid uses include compiling contacts for resale, building cold-email lead dumps, or extracting third-party addresses for unrelated monetization.

## Orange Data Mining / analysis guidance

- Orange or similar tooling may be used on first-party, licensed, or properly de-identified datasets.
- Remove direct identifiers where possible before clustering, scoring, or segmentation.
- If a workflow depends on named individuals, document the business purpose and retention limits.

## Decision protocol

Every new revenue idea must pass three gates:

1. Compliance gate: no hard prohibition triggered.
2. Scoring gate: evaluate with `instruments/strategy/score.sh`.
3. Mission log gate: record the decision in `docs/programs/agentic_financial_system/journal.md`.

## Default reframes for unsafe requests

- "Sell an email list" -> build an opt-in audience or a first-party CRM enrichment service.
- "Scrape inboxes for contacts" -> build an authorized inbox-to-CRM assistant for the mailbox owner.
- "Monetize scraped leads" -> build a research report, listing service, or content workflow using public or licensed data.

This document is the canonical compliance packet referenced by the financial-system program.
