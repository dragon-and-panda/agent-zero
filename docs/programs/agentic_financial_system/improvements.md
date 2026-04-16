# Agentic Financial System Improvements

This backlog tracks the highest-value improvements for turning the charter into an operational revenue system.

## Highest Priority

### 1. Inbox-to-CRM workflow definition
- Specify allowed Gmail or Google Workspace scopes.
- Define extraction schema for contacts, organizations, intents, and follow-ups.
- Separate "contact discovered" from "contact approved for CRM use."
- Add suppression and deletion handling.

### 2. Consent and provenance ledger
- Record how each customer record entered the system.
- Track whether the contact was opted in, customer-provided, or manually approved.
- Make provenance queryable from reports and logs.

### 3. Strategy scoring automation
- Expand the current scoring instrument into a repeatable intake checklist.
- Store score results with timestamps and operator notes.
- Add sample scorecards for PASS, HOLD, and REJECT cases.

### 4. Compliance injection into prompts
- Ensure monetization-focused personas always reference `docs/policies/compliance_pack.md`.
- Add negative examples for contact resale, spam, and non-consensual inbox use.

## Medium Priority

### 5. Listing-service commercialization path
- Convert `docs/autonomous_listing_service.md` into a narrower MVP offer.
- Define first target verticals and onboarding assets.
- Add success metrics that can be captured automatically.

### 6. Productized research templates
- Create reusable report templates for market scans, competitor analysis, and pricing briefs.
- Link output formats to clear delivery packages and pricing tiers.

### 7. Telemetry for autonomy economics
- Track intervention count, cycle time, and margin per lane.
- Identify which tasks remain manual and why.

## Lower Priority

### 8. CRM connectors and reversible sync
- Add safe connector patterns for common CRMs.
- Ensure records can be updated or removed cleanly.

### 9. Offer packaging and landing assets
- Build clearer offer statements, proposal outlines, and onboarding checklists for each lane.

### 10. Portfolio pruning rules
- Define when a lane should be paused, reworked, or retired based on economics and friction.
