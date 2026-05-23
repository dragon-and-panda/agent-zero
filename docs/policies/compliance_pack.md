# Compliance Pack for Autonomous Revenue Work

This pack defines the minimum legal, privacy, and platform-safety rules for any autonomous revenue workflow built in this repository.

## Non-negotiable prohibitions

The agent must not design, execute, or recommend workflows that:

- scrape, broker, rent, trade, or sell personal email addresses or contact lists
- extract inbox data from Google, Gmail, or any other mailbox without clear authorization from the account owner
- reuse contact data for a secondary purpose that the contact did not consent to
- send spam, evade rate limits, bypass platform controls, or hide sender identity
- bypass authentication, session controls, paywalls, or access restrictions
- misrepresent consent, data provenance, product claims, or financial results

## Required gates before activation

Every monetization lane must be screened for:

1. legality
2. consent
3. data provenance
4. platform and terms-of-service risk
5. unit economics
6. repeatability
7. automation fit

If legality, consent, or provenance is weak, or if platform risk is high, the lane must be rejected or held for redesign.

## Approved data-handling patterns

These patterns are allowed when the operator has rights to the data and the use matches the consented purpose:

- first-party CRM enrichment from customer-owned systems
- inbox-to-CRM extraction for the user's own mailbox or a client's mailbox with explicit authorization
- opt-in newsletter and lead-magnet funnels
- public, license-compatible business research datasets used within their terms
- operational analytics on data produced by the user's own products or services

## Approved revenue lanes for this program

Prefer lanes such as:

- agentic services sold to clients on clear contracts
- internal workflow automation with measurable savings
- research products, audits, and intelligence briefs
- listing, sourcing, and marketplace assistance that follows platform rules
- compliant inbox triage, CRM upkeep, and follow-up drafting for customer-owned accounts

## Gmail and mailbox RAG rules

RAG over mailbox content is only acceptable when all of the following are true:

- the mailbox owner explicitly authorized the use
- the use is limited to first-party productivity or a contracted client workflow
- the agent does not export or resell the contacts or message contents
- retention and access are limited to the stated business purpose

Mailbox RAG is not a license to compile or sell contact lists.

## Escalation rule

If a task mentions selling email lists, scraping contact details for resale, mass cold outreach from harvested data, or unclear inbox access rights, the agent must reject that lane and convert the goal into a compliant alternative.
