# Compliance Pack for Agentic Revenue Programs

This policy pack defines the minimum legal, ethical, and platform-compliance rules for any revenue-seeking workflow operated inside Agent Zero.

It applies to:
- autonomous outreach systems,
- inbox-processing or CRM workflows,
- lead-generation and sales operations,
- listing and marketplace automation,
- market research and data products,
- any future "financial system" or monetization program.

## 1. Non-Negotiable Prohibitions

The system must not:

1. harvest, scrape, purchase, broker, or sell personal email addresses or contact lists;
2. use a third party's inbox, Gmail account, or email archive without explicit authorization from the account owner;
3. send spam, unsolicited bulk messages, or deceptive outreach;
4. bypass platform Terms of Service, anti-bot controls, CAPTCHAs, or rate limits;
5. collect or process personal data without a lawful basis, clear provenance, and a legitimate business purpose;
6. misrepresent identity, affiliation, pricing, inventory, or outcomes;
7. enable fraud, impersonation, phishing, or gray-market lead trafficking.

Any workflow that depends on personal-email resale or non-consensual inbox access is automatically rejected.

## 2. Approved Revenue Lanes

The program should prioritize revenue streams with clear consent, clean provenance, and repeatable unit economics.

### Lane A: First-Party Inbox to CRM Operations
- Source: a user-owned or client-owned inbox with explicit authorization.
- Use case: summarize inbound demand, extract customer intents, deduplicate contacts, and route opted-in leads into a CRM.
- Guardrails:
  - only process data the owner is entitled to use;
  - preserve consent status;
  - maintain an audit trail of source and purpose;
  - never convert inbox data into a third-party resale list.

### Lane B: Opt-In Lead Generation
- Source: web forms, newsletter signups, referrals, booked calls, or client-owned subscriber lists.
- Use case: qualify leads, segment them, personalize compliant follow-up, and track conversions.
- Guardrails:
  - retain proof of opt-in where practical;
  - respect unsubscribe requests and suppression lists;
  - do not claim consent that was never obtained.

### Lane C: Research and Intelligence Products
- Source: public information, licensed datasets, first-party interview notes, and internally produced analysis.
- Use case: paid market maps, competitor briefs, niche trend trackers, procurement intelligence, or pricing reports.
- Guardrails:
  - cite sources;
  - avoid redistribution of restricted data;
  - separate factual claims from model inferences.

### Lane D: Autonomous Listing and Fulfillment Services
- Source: seller-provided assets and marketplace-compliant integrations.
- Use case: create listings, optimize descriptions, manage compliant marketplace operations, and support buyer communication.
- Guardrails:
  - follow each channel's policy requirements;
  - do not fabricate reviews, scarcity, or condition details;
  - escalate regulated or high-risk categories.

### Lane E: Internal Tooling and Service Delivery
- Source: internal workflows and customer-authorized business systems.
- Use case: data cleanup, SOP automation, reporting, support triage, and agent-managed operations for paying clients.
- Guardrails:
  - document access scopes;
  - minimize retained personal data;
  - keep permissions least-privilege.

## 3. Gmail / Email RAG Guardrails

Retrieval-augmented generation over email is allowed only when all of the following are true:

1. the inbox owner explicitly authorized the workflow;
2. the data source is lawful and contractually permitted;
3. the workflow has a defined business purpose, such as support triage, CRM enrichment, or opportunity classification;
4. outputs are used for internal operations or owner-authorized follow-up;
5. sensitive data is minimized, redacted, or excluded when not needed.

Disallowed examples:
- building a salable list of personal email addresses from mailbox contents;
- mining third-party inboxes for resale leads;
- auto-generating cold outreach targets from private correspondence.

Allowed examples:
- extracting support themes from a founder's own inbox;
- tagging inbound requests and routing opted-in prospects to a CRM;
- creating account summaries for a client engagement using the client's own records.

## 4. Orange DataScaping Usage Policy

If Orange DataScaping is used, it should operate as an analysis and organization layer for lawful, consented, or first-party datasets.

Suitable uses:
- deduplicating opted-in contacts,
- clustering inbound themes,
- segmenting customer requests,
- scoring opportunities from compliant lead sources,
- organizing research observations.

Unsuitable uses:
- laundering scraped personal data into a resale asset,
- combining unknown-provenance contact records,
- constructing "email lists for sale" from harvested sources.

## 5. Opportunity Scoring Requirements

Before any lane is activated, it must pass a structured scorecard:
- legality,
- consent quality,
- data provenance,
- Terms of Service compatibility,
- time to first cash,
- expected margin,
- repeatability,
- automation leverage,
- defensibility.

Hard-fail conditions:
- weak legality,
- weak consent,
- unclear provenance,
- known Terms-of-Service conflict.

These checks are implemented by `instruments/strategy/score.sh`.

## 6. Operating Rules for Autonomous Agents

Autonomous agents must:
- prefer consented first-party data over scraped or purchased data;
- preserve evidence for claims, contacts, and permissions;
- stop and reject workflows that depend on prohibited data acquisition;
- log major decisions, assumptions, and score results to mission journals;
- favor service delivery, software, research, and marketplace operations over gray-market data brokerage.

## 7. Phase 1 Monetization Direction

Phase 1 should focus on fast, compliant offers that can be delivered with current repo capabilities:

1. inbox-to-CRM triage for a user-owned mailbox;
2. autonomous listing and resale operations using seller-provided inventory;
3. paid research briefs or niche intelligence products;
4. opt-in lead qualification workflows for client-owned channels;
5. internal automation services sold to small businesses.

The system should treat contact-list resale as a rejected lane, not a backlog item.
