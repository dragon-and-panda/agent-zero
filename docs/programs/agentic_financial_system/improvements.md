# Agentic Financial System Improvements

## Priority Backlog

- [ ] Implement a Gmail-to-CRM ingestion path that only works on the user's own mailbox and only for first-party operational use.
- [ ] Add structured contact provenance fields before any CRM sync or enrichment step.
- [ ] Add a reusable evaluation prompt for offer selection, pricing, and channel fit.
- [ ] Create a reporting loop for margin, repeatability, and automation depth per lane.
- [ ] Add a watchdog extension that flags requests involving contact resale, spam, or non-consensual inbox extraction.
- [ ] Link future venture experiments back to `instruments/strategy/score.sh` outputs.

## Do Not Build

- [x] Email-list extraction and resale pipeline
- [x] Gmail scraping for bulk cold outreach inventory
- [x] Any workflow that treats private inbox data as a brokerage asset
