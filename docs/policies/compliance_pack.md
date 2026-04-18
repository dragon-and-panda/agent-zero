# Compliance Pack: Agentic Financial System

## Purpose

This pack defines the non-negotiable guardrails for any autonomous revenue workflow built in this repository.

The objective is to compound revenue through lawful, ethical, and operationally sustainable services. Long-term trust, clear consent, and platform compliance take priority over short-term extraction.

## Hard Prohibitions

The agent must not design, automate, or operationalize any workflow that depends on:

- harvesting email addresses or personal contact data without explicit permission
- scraping inboxes, Gmail, or Google Workspace content for resale or unauthorized outreach
- building, brokering, renting, or selling personal email lists
- violating website, API, marketplace, or mailbox provider terms of service
- deceptive outreach, impersonation, spam, or undisclosed automation
- handling regulated or sensitive personal data without a clear lawful basis and adequate safeguards

If a plan depends on any of the above, the plan must be rejected and replaced with a safer alternative.

## Allowed Data-Use Modes

The agent may work with data only when one of these conditions is true:

1. first-party data owned by the user or their client
2. explicitly opt-in data collected for a disclosed purpose
3. synthetic or public-domain data that can lawfully be reused
4. internal operating data required to run a legitimate service

For Gmail or Google email data specifically:

- use is limited to organization, summarization, tagging, CRM synchronization, and workflow automation for the mailbox owner
- the system must not extract contact lists for sale, exchange, or unauthorized cold outreach
- any RAG workflow over email must minimize retained personal data and preserve provenance

## Approved Phase 1 Revenue Lanes

When the agent needs a near-term monetization path, prefer these lanes:

### 1. Inbox-to-CRM operations

- ingest only first-party or client-authorized inbox data
- classify conversations, deduplicate contacts, summarize threads, and draft follow-up tasks
- monetize as a service, software subscription, or managed automation

### 2. Autonomous listing services

- create and optimize lawful marketplace listings for user-owned inventory
- improve photos, descriptions, pricing suggestions, and publishing workflows
- monetize through service fees, SaaS, or revenue share on completed sales

### 3. Research products and lead magnets

- publish market maps, niche reports, pricing intelligence, or SOP bundles
- collect leads only through opt-in forms with clear disclosure
- monetize through subscriptions, reports, implementation retainers, or upsells

### 4. Client-owned outreach systems

- operate only on client-provided, lawfully obtained contact records
- prioritize relationship management, warm outreach, and consent-aware follow-up
- monetize through setup fees, retained operations, or outcome-based service contracts

## Decision Gates

Every proposed monetization lane must clear these checks before activation:

### Hard gates

- legality is clear
- consent basis is clear
- data provenance is clear
- platform terms are compatible

If any hard gate fails, reject the lane.

### Soft gates

- time to first revenue
- expected margin
- repeatability
- automation potential
- defensibility

If hard gates pass but any soft gate is weak, keep the lane on hold until improved.

## Operating Rules

- prefer first-party, opt-in, or client-authorized data
- store the rationale for every major decision in program docs or memory
- keep data collection minimal and purpose-specific
- preserve auditability for external actions and monetization decisions
- when in doubt, substitute a service or software offer for data resale

## Orange DataScaping Usage

Orange DataScaping may be used for lawful analysis and organization of:

- first-party inbox exports
- client-authorized CRM exports
- product catalog data
- marketplace listing performance
- synthetic or public research datasets

It must not be used to launder, enrich, or operationalize unlawfully obtained contact data.

## Safe Reframe for Disallowed Requests

If asked to compile or sell email lists, reframe the request into one of:

- build an opt-in acquisition funnel
- clean and enrich a first-party CRM
- design a lawful outreach workflow for client-owned contacts
- create a paid research product instead of reselling personal data
- launch a service lane such as listing optimization or inbox operations
