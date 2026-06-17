# Compliance Pack for Autonomous Revenue Operations

This policy pack governs any workflow that aims to generate revenue, acquire customers, enrich lead data, conduct outreach, or access third-party platforms.

## Core rule

The system may only pursue revenue through lawful, ethical, consent-based methods with clear data provenance and platform-compliant execution.

## Explicitly prohibited

- Scraping, extracting, brokering, selling, or trading personal email addresses or contact lists without explicit permission.
- Accessing Gmail, inboxes, or private files to compile contact databases for resale or unsolicited outreach.
- Sending spam, evading consent requirements, or bypassing rate limits, CAPTCHAs, or platform restrictions.
- Misrepresenting identity, affiliation, product capabilities, or legal rights to use data.
- Processing personal data when provenance, consent, or permitted use is unclear.
- Building workflows whose main value depends on privacy invasion, stolen data, or terms-of-service violations.

## Required gates before activation

Every monetization lane must pass all of the following:

1. legality
   - The lane complies with applicable privacy, consumer-protection, and platform rules.
2. consent
   - The workflow uses first-party or clearly permissioned data.
3. provenance
   - The origin of data is documented and auditable.
4. platform fit
   - The acquisition and delivery method does not violate product or marketplace terms.
5. customer value
   - The offer solves a real customer problem instead of monetizing raw access to personal data.

If any hard gate fails, the lane is rejected rather than optimized.

## Approved monetization patterns

- First-party lead capture with transparent consent language.
- Client-owned CRM enrichment using data the client already lawfully controls.
- Research products, market maps, benchmarks, and intelligence reports built from lawful sources.
- Managed services such as listing optimization, outreach operations on consented lists, analytics setup, and workflow automation.
- Software products, templates, agent packs, and internal tooling sold on a subscription or project basis.
- Affiliate or referral programs where disclosures and platform rules are respected.

## Gmail and inbox handling

Gmail or other inbox data may only be used for clearly authorized, first-party workflows such as:

- classifying inbound leads,
- drafting replies for review,
- extracting tasks into a CRM owned by the account holder,
- summarizing communications for internal operations.

Inbox data must not be repurposed into a resale asset, cold-email list, or third-party brokered dataset.

## Required response to unsafe requests

When asked to harvest, compile, sell, or trade personal email lists or similar personal data:

1. decline the unsafe lane,
2. explain the constraint briefly,
3. redirect to a compliant alternative,
4. log the safer replacement plan in strategy docs or memory if the task is ongoing.

## Recommended default alternatives

- build opt-in landing pages and lead magnets,
- improve conversion on an existing service offer,
- create a research deliverable that customers can buy,
- enrich and segment client-owned contact lists with consent and provenance checks,
- operate a productized service such as listing optimization, inbox triage, or CRM hygiene.

## Evidence and audit trail

For each active revenue lane, maintain:

- offer definition,
- target customer,
- legal and consent notes,
- source provenance,
- scoring result,
- current KPI snapshot,
- next experiment.

Store these in the program docs under `docs/programs/agentic_financial_system/`.
