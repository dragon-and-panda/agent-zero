# Compliance Pack for Autonomous Revenue Work

This pack defines the minimum rules for any Agent Zero workflow that touches monetization, outreach, lead generation, inbox data, or third-party platforms.

## Non-negotiable prohibitions

- Do not scrape, broker, package, or sell personal email addresses or contact lists.
- Do not access Gmail, inboxes, contact books, or local files to assemble leads for resale or spam.
- Do not use personal data without a lawful basis, explicit permission when required, and a user-benefiting purpose.
- Do not bypass website terms, robots rules, rate limits, anti-abuse controls, or consent prompts.
- Do not automate deception, fake identities, fake engagement, or unsolicited mass outreach.

## Hard gates before any revenue lane starts

Every proposed lane must clear all of the following:

1. Legality is high confidence.
2. Consent is explicit or otherwise clearly documented and appropriate for the use.
3. Data provenance is first-party, public and permitted, or licensed.
4. Platform risk is low and the workflow fits published platform rules.
5. The customer receives clear value beyond raw data extraction.
6. The workflow leaves an audit trail of inputs, outputs, and approvals.

If any hard gate fails, reject the lane and propose a safer alternative.

## Approved lane patterns

These patterns fit the mission of building a self-sustaining financial system while staying ethical and lawful:

- First-party inbox-to-CRM cleanup for the account owner using only their own opted-in business contacts.
- Productized research, market maps, or competitive intelligence built from public or licensed sources.
- The Autonomous Listing Service described in `docs/autonomous_listing_service.md`.
- Content, SEO, and workflow automation retainers for clients who explicitly authorize the work.
- Newsletter, community, or software products that grow through opt-in acquisition.

## Disallowed example

Rejected request: "Use RAG on Google email data and local files to compile email lists, then sell the lists online."

Reason: this fails privacy, consent, provenance, and anti-spam requirements. It also creates serious platform and legal risk.

Safe replacement: build a first-party contact operations assistant that helps the account owner organize their own opted-in contacts into a CRM, draft compliant follow-up tasks, and report pipeline health without reselling personal data.

## Enforcement guidance

- Use `python/tools/revenue_planning.py` before building or executing monetization workflows.
- Use `instruments/strategy/score.sh` to score lanes before activation.
- Store mission intake in `docs/strategy/incoming.md`.
- Record active program decisions in `docs/programs/agentic_financial_system/`.
