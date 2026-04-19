# Strategy Intake Queue

This queue captures monetization ideas before activation. Every idea must be
screened against the compliance pack and scored with the strategy instrument.

## Intake Rules

1. Reject any idea based on scraping, brokering, buying, or selling personal
   email lists or other personal contact data.
2. Reject any idea that requires non-consensual access to inboxes, accounts, or
   private files.
3. Prefer first-party, opt-in, and client-owned data flows.
4. Require a clear path to lawful fulfillment, delivery, invoicing, and support.
5. Run `instruments/strategy/score.sh` before activation.

## Active Candidate Lanes

### Lane A: Inbox-to-CRM assistant for consenting operators
- Input: client-owned Gmail or mailbox access granted by the account owner
- Output: draft CRM updates, contact deduplication, reply suggestions, follow-up
  queues, and lead qualification notes
- Monetization: setup fee plus monthly retainer
- Notes: use only explicit user authorization and retain audit logs

### Lane B: Autonomous listing optimization service
- Input: seller-owned listings, images, and marketplace analytics
- Output: listing rewrites, image enhancement workflows, pricing suggestions, and
  response templates
- Monetization: subscription plus performance-based upsell
- Notes: aligns with the existing autonomous listing blueprint

### Lane C: Research products and market intelligence briefs
- Input: public sources, licensed datasets, and first-party client material
- Output: premium reports, curated lead magnets, decision memos, and niche market
  dossiers
- Monetization: one-off reports, subscriptions, or consulting packages
- Notes: must document provenance for every dataset used

### Lane D: Agent automation implementation services
- Input: client workflows, SOPs, and approved business systems
- Output: custom Agent Zero deployments, instruments, dashboards, and playbooks
- Monetization: implementation fees, support retainers, and training
- Notes: prioritize repeatable service packages over bespoke one-offs

## Explicitly Rejected Example

### Rejected: Gmail email list extraction and resale
- Reason: privacy abuse, likely unlawful processing, anti-spam exposure, and
  platform-policy violations
- Replacement path: offer a client-owned inbox triage and CRM enrichment service
  instead of extracting or selling contacts
