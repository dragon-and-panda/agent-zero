# Incoming Opportunities Queue

Use this file as the intake lane described in `docs/autonomous_super_agency.md`. Every new revenue concept should be written here, scored with `instruments/strategy/score.sh`, and then labeled `GO`, `HOLD`, or `REJECT`.

---

## Decision Standard

An opportunity is eligible for execution only if it is:

- Legal
- Consent-based
- Operationally auditable
- Automatable without obvious platform abuse
- Capable of surviving interruptions with bounded downside

---

## GO Examples

### 1. Consent-Based Inbox-to-CRM Hygiene Service
- **Offer:** For a business that owns the inbox, ingest mailbox threads with permission, extract customer and supplier records, deduplicate them, and push structured records into a CRM.
- **Why it qualifies:** The mailbox owner authorizes access, the work creates business value, and the system does not resell private data.
- **Tooling angle:** RAG over approved mailbox content, Orange-based clustering/segmentation, audit logs, opt-out handling.

### 2. Autonomous Listing Concierge
- **Offer:** Turn seller photos and notes into high-quality marketplace listings and manage buyer interactions within guardrails.
- **Why it qualifies:** Clear value exchange, consent from the seller, reusable automation, multiple pricing models.
- **Repo anchor:** `docs/autonomous_listing_service.md`

### 3. Tutorial + Course + Affiliate Funnel
- **Offer:** Document the build process, publish tutorials, package templates/checklists, and monetize with affiliates, sponsorships, or paid downloads.
- **Why it qualifies:** Uses original content, compounds over time, and diversifies revenue beyond service delivery.

### 4. Lead Qualification for Opt-In Audiences
- **Offer:** Analyze contacts from a newsletter, waitlist, or customer list that already opted in, then segment and prioritize them for follow-up.
- **Why it qualifies:** Consent exists, value is analytical rather than extractive, and Orange can help with clustering and visual analysis.

---

## HOLD Examples

### 1. Gmail Knowledge Assistant for Internal Operations
- **Idea:** Build a private assistant that summarizes a founder's or team's own inbox and drafts replies.
- **Why HOLD:** Useful and compliant when scoped correctly, but requires consent records, retention limits, and a clear export policy before activation.

### 2. Trading Research Stack
- **Idea:** Backtest Forex or other strategies and maintain a paper-trading journal.
- **Why HOLD:** Acceptable as research, but live deployment must wait until risk controls and operating reserves are in place.

---

## REJECT Examples

### 1. Harvest Gmail Addresses and Sell the List
- **Why REJECT:** Violates privacy expectations, fails consent requirements, creates legal and reputational exposure, and depends on personal-data brokerage.
- **Replacement:** Offer inbox cleanup, CRM migration, or opt-in segmentation for the mailbox owner.

### 2. Bulk Outreach From Received/Sent/CC History
- **Why REJECT:** Treats unrelated correspondents as leads without permission and would push the system toward spam behavior.
- **Replacement:** Build campaigns only from opt-in or customer-authorized records.

### 3. Immediate Live Forex Deployment as Primary Revenue Engine
- **Why REJECT:** Puts operating capital at risk before the system has stable compliant cash flow.
- **Replacement:** Keep trading in research mode until the treasury policy gates are met.

---

## Activation Sequence Once Resources Are Sufficient

When the system has baseline infrastructure, logs, and at least one validated offer, activate the revenue stack in this order:

1. **Service lane:** Launch the consent-based inbox-to-CRM hygiene service.
2. **Marketplace lane:** Run the autonomous listing concierge for redundant cash flow.
3. **Content lane:** Publish the build log, tutorial assets, and affiliate-backed education content.
4. **Treasury lane:** Allocate only ring-fenced surplus cash to simulation first, then tightly bounded live trading if risk gates are passed.

This ordering reduces dependency on any single acquisition source and creates redundancy across service, product, and content revenue.
