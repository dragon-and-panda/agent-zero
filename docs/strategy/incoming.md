# Strategy Intake Queue

Use this file to capture candidate ventures before activation. Every entry should be scored with `instruments/strategy/score.sh` and aligned to `docs/policies/compliance_pack.md`.

## Intake template

```text
- lane:
  description:
  customer:
  data source:
  consent model:
  legality:
  platform risk:
  monetization:
  notes:
  score result:
```

## Current queue

- lane: inbox-to-CRM assistant
  description: extract structured opportunities, contacts, and summaries from a customer-owned mailbox into the customer's CRM
  customer: small service businesses and operators with shared inboxes
  data source: customer-owned mailbox or Google Workspace account with explicit authorization
  consent model: first-party operational use only
  legality: strong if authorization and data handling controls are documented
  platform risk: medium
  monetization: setup fee plus recurring operations retainer
  notes: best near-term fit for existing RAG and workflow capabilities
  score result: pending

- lane: autonomous listing operations
  description: enrich owner-provided listing data and automate publishing support
  customer: marketplace sellers and property or catalog operators
  data source: owner-provided product, asset, or listing records
  consent model: first-party owner data
  legality: strong
  platform risk: medium
  monetization: managed service or subscription
  notes: aligns with `docs/autonomous_listing_service.md`
  score result: pending

- lane: contact-list brokerage
  description: compile email lists from inboxes or files and sell them
  customer: not applicable
  data source: personal or mailbox-derived contacts
  consent model: weak or absent
  legality: unacceptable
  platform risk: high
  monetization: prohibited
  notes: reject per compliance pack; do not revisit without a materially different, permissioned model
  score result: reject
