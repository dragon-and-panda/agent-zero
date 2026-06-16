# Strategy Intake Queue

Use this file as the landing zone for new monetization ideas before they are activated.

## Status legend

- PASS: compliant and attractive enough to pilot
- HOLD: compliant or salvageable, but missing proof or economics
- REJECT: conflicts with policy or depends on abusive tactics

## Queue

### REJECT - personal email list brokerage

- idea: extract email addresses from Google email data and other files, then sell the lists
- reason: violates `docs/policies/compliance_pack.md`
- blockers:
  - no consent from contacts
  - private inbox data proposed for resale
  - likely privacy, anti-spam, and terms-of-service violations
- pivot:
  - use mailbox RAG only for the owner's own inbox
  - convert inbound leads into a client-owned CRM

### PASS - inbox-to-CRM assistant

- idea: summarize a consenting owner's inbound email, classify commercial intent, and draft CRM-ready records
- data: first-party inbox or explicit client authorization only
- revenue model: setup fee plus monthly automation retainer
- next step: score with `instruments/strategy/score.sh` and define a pilot schema

### HOLD - niche public-data research subscription

- idea: build a recurring report from public, licensed, or aggregated sources
- concern: niche selection and willingness-to-pay are not yet validated
- next step: choose one niche and score it before building

### PASS - autonomous listing operations service

- idea: monetize listing generation and merchandising workflows for consenting clients
- repo anchor: `docs/autonomous_listing_service.md`
- next step: attach telemetry and define pricing packages
