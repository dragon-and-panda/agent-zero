# Strategy Intake Queue

Use this queue to capture new monetization ideas before any implementation begins.

## Required fields

- idea
- target customer
- value created
- data source and ownership
- consent model
- platform dependencies
- score status

## Current queue

| Idea | Status | Notes |
| --- | --- | --- |
| Client-owned inbox to CRM operations | Active candidate | Allowed only for user-owned or client-authorized inboxes. Monetize the workflow, not the contact data. |
| Autonomous listing operations | Active candidate | Aligns with `docs/autonomous_listing_service.md`. |
| Research and intelligence subscriptions | Active candidate | Use public sources, licensed sources, and client-owned data only. |
| Sell harvested email lists from Gmail or other files | Rejected | Violates consent, privacy, provenance, and anti-spam requirements. Replace with opt-in audience growth or client-owned CRM services. |

## Intake rule

Any idea involving non-consensual inbox access, contact harvesting, credential misuse, spam, or personal-data resale is rejected on intake and redirected to a compliant equivalent.
