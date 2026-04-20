# Strategy Intake Queue

## Intake rules

- Every new revenue idea must be evaluated for legality, consent, provenance,
  and platform fit before build work starts.
- If the idea relies on personal-data resale, inbox scraping without explicit
  authorization, or spam, mark it `REJECT` and replace it with a compliant lane.
- Use `python/tools/revenue_planning.py` for structured screening and
  `instruments/strategy/score.sh` for a simple go/hold/reject score.

## Current queue

### REJECT: broker or sell compiled email lists
- Why rejected: depends on personal-data resale, unclear consent, and high
  platform and legal risk.
- Compliant replacement: build an Inbox-to-CRM assistant for user-owned mail,
  or build public research products from lawful public sources.

### ACTIVE: Inbox-to-CRM assistant for authorized mailboxes
- Goal: convert inbound email into summaries, lead records, and next-action
  queues for the mailbox owner.
- Data basis: first-party or explicitly authorized mailbox access only.
- Analysis: Orange DataScaping may be used only on authorized, first-party,
  or public-source exports.

### ACTIVE: public-source research products
- Goal: sell curated market intelligence, benchmark packs, or directories built
  from lawful public data with provenance notes.

### ACTIVE: listing and marketplace operations
- Goal: provide operational services for client-owned listings, catalogs, or
  directories using Agent Zero automation.
