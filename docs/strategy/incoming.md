# Strategy Intake Queue

Use this file as the intake surface for new autonomous missions. Every idea must be scored with `instruments/strategy/score.sh` before activation.

## Decision labels
- **GO**: Legally/ethically viable, inside current capability, and worth near-term exploration.
- **HOLD**: Potentially viable, but blocked by missing assets, approvals, proof, or economics.
- **REJECT**: Violates compliance rules, lacks consent, or depends on deceptive / unlawful tactics.

## Current examples

### GO: Consent-based Inbox-to-CRM Hygiene Service
- **Description:** With explicit client authorization, ingest the client's business inbox data, classify inbound demand, extract opted-in contacts, and sync structured records into a CRM.
- **Why it fits:** First-party data, permissioned access, immediate business value, recurring service revenue.
- **Next action:** Build a sandbox ingestion + classification workflow using imported knowledge and client-owned mailbox exports.

### GO: Autonomous Listing Service
- **Description:** Turn seller photos and notes into improved marketplace listings and assist with compliant buyer communications.
- **Why it fits:** Clear user value, no dependency on personal data brokerage, can start from the existing service scaffold.
- **Next action:** Scope MVP hardening and telemetry instrumentation.

### HOLD: Research products / market intelligence subscriptions
- **Description:** Publish paid reports, datasets, and automation playbooks built from lawful public and licensed sources.
- **Why it fits:** High-margin and reusable, but requires packaging, audience validation, and distribution.
- **Next action:** Prototype one narrow report and pricing test.

### REJECT: Personal email list harvesting and resale
- **Description:** Extract emails from inboxes or other files and sell the resulting lists to online services.
- **Why it is rejected:** Lacks consent, creates privacy and anti-spam risk, and conflicts with the compliance pack.
- **Replacement pattern:** Offer opt-in lead generation, client-owned CRM cleanup, or lawful audience research instead.
