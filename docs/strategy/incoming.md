# Incoming Strategy Queue

Use this file as the intake queue for new revenue ideas before execution.

## Intake Template

- lane:
- description:
- data sources:
- monetization model:
- operator authorization:
- consent quality:
- provenance quality:
- platform-risk level:
- expected margin:
- expected repeatability:
- notes:

## Queue

### REJECTED: Contact-list brokerage from inbox or file extraction

- lane: personal email list brokerage
- description: extract email addresses from Gmail and local files, organize them, then sell the compiled list
- data sources: inbox data and unspecified files
- monetization model: resale of personal contact data
- operator authorization: unclear
- consent quality: low
- provenance quality: low
- platform-risk level: high
- notes: violates the compliance pack; do not execute

### HOLD: Owner-authorized inbox to CRM automation

- lane: client-owned inbox operations
- description: use RAG on an owner-authorized mailbox to classify, summarize, deduplicate, and sync inbound leads into the client's CRM
- data sources: client-owned mailbox and CRM
- monetization model: paid service or software subscription
- operator authorization: high
- consent quality: medium until the client confirms allowed downstream use
- provenance quality: high
- platform-risk level: medium
- notes: activate only after downstream use, retention, and unsubscribe handling are documented

### PASS CANDIDATE: Research products from public business data

- lane: research briefs
- description: compile public business information into niche reports and recurring intelligence products
- data sources: public company sites, directories, filings, and operator-created analysis
- monetization model: subscription or one-off report sales
- operator authorization: high
- consent quality: high
- provenance quality: high
- platform-risk level: low
- notes: run through `revenue_planning` and `instruments/strategy/score.sh` before activation

### PASS CANDIDATE: Autonomous listing services

- lane: listings
- description: generate, enrich, and publish marketplace or directory listings for paying clients
- data sources: client-provided catalogs, assets, and public listing rules
- monetization model: setup fee plus recurring management
- operator authorization: high
- consent quality: high
- provenance quality: high
- platform-risk level: low
- notes: align with `docs/autonomous_listing_service.md`
