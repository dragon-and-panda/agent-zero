# Compliance Pack for Autonomous Revenue Systems

This policy pack defines the minimum legal, privacy, and ethical standards for
any revenue-generating workflow built in this repository.

## 1. Purpose

The objective is to build autonomous and semi-autonomous systems that create
revenue while remaining:

- legal in the operating jurisdiction,
- consistent with platform terms of service,
- respectful of privacy and consent,
- auditable by future agents and human reviewers.

This pack is the canonical guardrail referenced by the Compliance Guardian and
the Risk & Ethics Governor described in `docs/autonomous_super_agency.md`.

## 2. Hard Prohibitions

The following activities are not allowed:

1. Harvesting personal email addresses, phone numbers, or contact lists from
   Gmail, local files, scraped pages, or third-party systems for resale.
2. Selling, brokering, renting, or packaging personal contact data without
   explicit, documented permission from the data subject and a lawful basis.
3. Accessing inboxes, CRMs, or cloud accounts without the owner's informed,
   revocable authorization.
4. Sending or enabling spam, deceptive outreach, impersonation, or undisclosed
   automated solicitation.
5. Circumventing site rules, CAPTCHAs, rate limits, or anti-bot controls where
   doing so violates law or platform policy.
6. Using sensitive personal data for monetization without a domain-specific
   compliance review.

Any mission that depends on these behaviors must be rejected, logged as
non-compliant, and replaced with a lawful alternative.

## 3. Allowed Data Classes

Only the following data classes may be used in revenue workflows:

| Class | Description | Allowed Use |
| --- | --- | --- |
| Owner-controlled first-party data | Data from the operator's own accounts, inboxes, and systems | Allowed with purpose limitation and retention controls |
| Client-authorized operational data | Data from a paying client who has granted permission | Allowed only for the contracted purpose |
| Explicitly opted-in leads | Contacts who knowingly requested communication | Allowed for the promised purpose and cadence |
| Public business information | Publicly available business contact details with clear commercial relevance | Allowed only if outreach remains compliant and non-deceptive |
| Licensed commercial datasets | Purchased data with verified redistribution/use rights | Allowed only within license scope |

## 4. Disallowed Data Classes

The following data classes are prohibited for activation:

- Personal email addresses extracted from inboxes for resale.
- Contact lists gathered from unclear provenance.
- Any data whose source, consent, or licensing cannot be documented.
- Credentials, secrets, tokens, session cookies, or private communications
  gathered for monetization.

## 5. Rules for Email and RAG

Email ingestion is allowed only under the following conditions:

1. The mailbox belongs to the operator or a client who granted explicit access.
2. The purpose is operational assistance, such as triage, CRM updates, support,
   invoicing, or follow-up on existing business relationships.
3. Retrieval must minimize scope to the current task rather than bulk-exporting
   entire histories.
4. Retention must be limited to summaries, task metadata, or approved records
   rather than raw message dumps whenever possible.
5. Third-party contact details surfaced during retrieval must not be sold,
   transferred, or repurposed into a cold-outreach list.

Approved examples:

- summarizing inbound purchase requests,
- extracting action items for the mailbox owner,
- creating a first-party CRM of existing customer conversations,
- building a support knowledge base from the owner's prior sent/received mail.

Rejected examples:

- compiling all discovered email addresses into a sellable asset,
- scraping mailing lists from archived mailboxes,
- converting unrelated inbound contacts into a cold outbound database.

## 6. Compliance Gates Before Any Launch

Every new monetization lane must pass all of the following:

1. **Lawfulness:** There is a plausible lawful basis and no obvious privacy or
   consumer-protection conflict.
2. **Consent/Authority:** The operator owns the data or has explicit written
   permission to process it.
3. **Terms of Service:** The workflow does not depend on prohibited automation,
   scraping, resale, or impersonation.
4. **User Benefit:** The product creates legitimate value for the customer.
5. **Auditability:** A future reviewer can inspect source, purpose, and major
   decisions from repository artifacts.

If any gate fails, the lane is marked `REJECT`.

## 7. Preferred Revenue Lanes

When a proposed lane fails the above gates, pivot to one of these compliant
patterns:

1. Opt-in lead capture and CRM enrichment.
2. Client-owned inbox automation and workflow ops.
3. AI-assisted listing, resale, and marketplace services.
4. Productized research, monitoring, and intelligence reports.
5. Digital assets, templates, courses, or internal tools sold directly.
6. Service businesses where automation reduces delivery cost rather than
   monetizing private data.

## 8. Required Artifacts

Before activating any lane, create or update:

- `docs/strategy/incoming.md` for the intake and safe framing,
- `docs/programs/<mission>/charter.md` for scope and KPIs,
- `docs/programs/<mission>/journal.md` for decision logging,
- `docs/programs/<mission>/improvements.md` for backlog and experiments,
- `instruments/strategy/score.sh` output showing the lane passed gates.

## 9. Enforcement

- The scoring instrument must reject any lane with weak legality, unclear data
  provenance, or non-consensual contact monetization.
- Mission diaries must record rejected ideas so later runs do not revisit them
  without new facts.
- If an active workflow drifts into prohibited behavior, the lane should be
  paused immediately and re-scoped before further execution.

## 10. Default Position for This Repository

The current default posture is:

- **Yes:** owner-authorized inbox operations, opt-in lead systems, lawful
  marketplace automation, research products, and software/service monetization.
- **No:** extracting and selling personal email lists, privacy-invasive data
  brokerage, spam infrastructure, and non-consensual contact acquisition.
