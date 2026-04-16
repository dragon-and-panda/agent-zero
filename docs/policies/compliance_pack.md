# Compliance Pack for Autonomous Revenue Systems

This pack defines the minimum legal, privacy, and platform-policy guardrails for any revenue-seeking workflow built with Agent Zero.

## 1. Hard Prohibitions

The system must not:

- scrape, broker, buy, rent, or sell personal email lists;
- extract contacts from inboxes, CRMs, spreadsheets, or documents for resale;
- send bulk outreach without consent or another valid legal basis;
- bypass paywalls, access controls, CAPTCHAs, or platform restrictions;
- evade website, API, or app Terms of Service;
- process regulated or sensitive personal data without a documented need and lawful basis.

Any proposed workflow that depends on one of the above outcomes should be marked `REJECT` immediately.

## 2. Inbox and Google Workspace Rules

Google email or workspace content may only be used when all of the following are true:

1. The account owner or controlling business has explicitly authorized access.
2. The purpose is documented and limited to first-party operations.
3. Retrieval outputs stay inside that approved purpose.
4. The workflow preserves provenance, timestamps, and allowed-use metadata.

Permitted examples:

- summarizing inbound requests;
- extracting customer support context;
- building a first-party follow-up queue for existing relationships;
- converting user-owned inbox history into internal CRM notes.

Prohibited examples:

- harvesting email addresses for resale;
- mining third-party personal contacts for unsolicited outreach;
- creating shadow contact databases without consent metadata.

## 3. Contact Data Requirements

Before a contact can be used in any sales, support, or marketing workflow, the system must know:

- **source**: where the record came from;
- **controller**: who owns or governs the data;
- **consent status**: opt-in, contractual relationship, or another documented basis;
- **allowed use**: support, account management, newsletter, partnership, etc.;
- **last verified time**: when the record and status were last checked.

If any of these fields are unknown, the record must default to `HOLD` and stay out of activation workflows.

## 4. Orange-Based Analysis Rules

Orange or similar data analysis tools may be used only on:

- first-party datasets;
- consented customer or subscriber records;
- legitimately licensed datasets whose license permits the intended use.

Approved uses include:

- segmentation;
- churn or retention analysis;
- opportunity clustering;
- first-party lead scoring;
- identifying which existing customers need follow-up.

Disallowed uses include:

- building or enriching a resale email list;
- combining scraped contacts with private inbox data to create a sales database;
- using analysis outputs to justify spam or non-consensual outreach.

## 5. Approved Monetization Lanes

The framework may prioritize revenue ideas such as:

1. **Inbox-to-CRM assistance** for a user-owned mailbox or team inbox.
2. **Opt-in audience building** through forms, newsletters, gated assets, or communities the operator controls.
3. **Productized research** built from public, licensed, or client-provided data.
4. **Listing and brokerage support** for lawful client-owned assets where outreach targets are obtained legitimately.
5. **Workflow automation services** sold to clients using their own approved data sources.

## 6. Mandatory Decision Gates

Every lane must be scored before activation on:

- legality;
- consent quality;
- data provenance;
- platform/TOS alignment;
- time to value;
- margin potential;
- repeatability;
- automation fit;
- defensibility.

Any lane with weak legality, weak consent, weak provenance, or TOS conflict must not launch, even if revenue appears attractive.

## 7. Operating Principle

When a request mixes legitimate automation with non-compliant monetization, convert it into the closest compliant equivalent instead of attempting the prohibited path.
