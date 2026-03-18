# Strategy Intake Queue

Use this file as the front door for new opportunities before spinning up agents or instruments.

---

## 1. Intake Template

Record each idea with the following fields:

| Field | Description |
| --- | --- |
| Idea | Short description of the offer or experiment |
| Customer | Who pays for it |
| Data Source | Owned, client-owned, public, or third-party |
| Consent Status | Explicit, implied business relationship, unknown, or none |
| Revenue Model | Setup fee, retainer, subscription, one-off, affiliate, etc. |
| Automation Fit | Low / Medium / High |
| Time to Cash | Slow / Medium / Fast |
| Legal or Platform Risk | Low / Medium / High |
| Backup Path | What happens if the main channel fails |
| Initial Verdict | GO / HOLD / REJECT |

---

## 2. Decision Rules

- **GO**
  - Consent is clear.
  - Data source is owned, client-owned, or lawfully public.
  - Revenue path is direct and testable.
  - At least one fallback channel exists.

- **HOLD**
  - The idea may be legal, but delivery, positioning, or risk controls are not mature yet.
  - It depends on regulated activity, new infrastructure, or unclear market demand.

- **REJECT**
  - The idea depends on privacy invasion, spam, scraping hidden personal data, or resale of contact information.
  - The main revenue path is unethical, deceptive, or likely to violate platform rules.

---

## 3. Example Queue

### GO — Inbox-to-CRM Hygiene Service
- **Customer:** founder, freelancer, small business owner
- **Data Source:** client-owned mailbox
- **Consent Status:** explicit
- **Revenue Model:** setup fee + monthly retainer
- **Automation Fit:** high
- **Time to Cash:** fast
- **Backup Path:** pivot from Gmail cleanup to CRM cleanup or follow-up automation
- **Why:** uses the client's own data for the client's benefit and can expand into broader automation work

### GO — Autonomous Listing Concierge
- **Customer:** local sellers and resellers
- **Data Source:** seller-supplied product photos and notes
- **Consent Status:** explicit
- **Revenue Model:** per-listing fee + premium upsells
- **Automation Fit:** high
- **Time to Cash:** fast
- **Backup Path:** if one marketplace underperforms, syndicate to others

### GO — Tutorial / Course / YouTube Content Engine
- **Customer:** audience, buyers of templates or courses, inbound clients
- **Data Source:** internally created workflows and case studies
- **Consent Status:** explicit
- **Revenue Model:** course sales, affiliate revenue, inbound leads
- **Automation Fit:** medium
- **Time to Cash:** medium
- **Backup Path:** repurpose into blog posts, lead magnets, and sales collateral

### HOLD — Forex Trading Program
- **Customer:** none initially; capital deployment activity
- **Data Source:** market data
- **Consent Status:** not applicable
- **Revenue Model:** speculative gains
- **Automation Fit:** medium
- **Time to Cash:** unknown
- **Backup Path:** keep in paper-trading mode until service revenue funds the reserve
- **Why:** should not be the first revenue layer; requires stronger risk controls and proof discipline

### REJECT — Email List Brokerage from Gmail Archives
- **Customer:** list buyers
- **Data Source:** inbox, sent mail, CC fields, attachments
- **Consent Status:** none
- **Revenue Model:** sale of harvested contacts
- **Automation Fit:** high
- **Time to Cash:** potentially fast
- **Backup Path:** none that preserves the same tactic
- **Why:** violates the compliance pack; replace with a first-party CRM cleanup service
