# Strategy Intake Queue

Use this page to capture new missions before they enter the super-agency
workflow. Each candidate lane should be scored for legality, consent,
repeatability, time-to-cash, operator fit, capital needs, and downside.

## Intake template

| Field | Notes |
| --- | --- |
| Mission name | Short label |
| Problem solved | What the buyer gets |
| Data source | Who owns the data and why it is lawful to use |
| Revenue model | Fixed fee, retainer, commission, product, subscription |
| Delivery model | Manual, agent-assisted, or automated |
| Primary risks | Legal, platform, ops, reputation, capital |
| Contingency | What happens if the lane stalls or fails |
| Score | Output from `instruments/strategy/score.sh` |

## Current queue examples

### GO — Inbox-to-CRM Hygiene Service

- **Problem solved:** turn a client's own inbox/export into a clean CRM import
  with deduped contacts, company grouping, and consent tagging
- **Data source:** client-owned Google Workspace or mailbox export only
- **Tooling:** RAG for retrieval over the client's authorized records, Orange
  Data Mining for clustering and cleanup, spreadsheet/CSV export
- **Revenue model:** setup fee plus optional monthly hygiene retainer
- **Contingency:** if inbox access is blocked, operate from a customer-supplied
  CSV export instead

### GO — Autonomous Listing Concierge

- **Problem solved:** create and manage premium marketplace listings for local
  sellers or small businesses
- **Data source:** seller-supplied photos, notes, and product information
- **Revenue model:** listing package fee, success fee, or managed-service
  retainer
- **Contingency:** if a platform adapter fails, publish a ready-to-post package
  and keep other platforms active

### HOLD — Course and YouTube Story Engine

- **Problem solved:** document the system and repurpose learnings into a
  tutorial, case study, and narrated YouTube format
- **Creative angle:** anthropomorphic narrator telling the story of funding a
  mech-suit and robot-body ambition
- **Revenue model:** ads, affiliates, consulting funnel, digital products
- **Reason for HOLD:** activate after there is enough real process evidence to
  make the material credible

### HOLD — Trading Research Sandbox

- **Problem solved:** test capital-allocation ideas in simulation before live
  exposure
- **Revenue model:** none initially; this is a risk-managed research lane
- **Reason for HOLD:** requires written rules, reserves, and paper-trade
  metrics before any live capital is considered

### REJECT — Personal Email List Brokerage

- **Reason:** depends on harvesting or compiling contacts from received/sent/CC
  data for resale or unsolicited outreach
- **Status:** prohibited by `docs/policies/compliance_pack.md`

### REJECT — Immediate Live Forex Without Guardrails

- **Reason:** speculative capital deployment without simulation history,
  reserve policy, or drawdown controls
- **Status:** prohibited until risk gates are met
