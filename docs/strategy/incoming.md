# Strategy Intake Queue

This file is the intake queue for autonomous revenue programs. Each candidate lane should be scored with `instruments/strategy/score.sh` before activation.

## Status Key

- `NEW` - proposed, not yet scored
- `HOLD` - lawful but not attractive enough to activate yet
- `ACTIVE` - approved and currently receiving execution effort
- `REJECTED` - blocked for legality, consent, TOS, or weak economics

---

## Current Candidates

### 1. Inbox-to-CRM Service for Client-Owned Inbound Leads
- Status: `ACTIVE`
- Why: Strong legality when owner-authorized, clear operational value, good automation fit
- Notes: Focus on summarization, routing, tagging, and follow-up drafting for first-party inbound messages only

### 2. Autonomous Listing Service
- Status: `ACTIVE`
- Why: Adjacent to the existing repo blueprint and does not rely on personal-data resale
- Notes: Prioritize listing creation, channel-specific compliance, and seller workflow automation

### 3. Research Products and Market Maps
- Status: `HOLD`
- Why: Lawful and productizable, but depends on selecting a narrow niche with stronger demand evidence
- Notes: Use licensed or lawful public sources only

### 4. Opt-In Lead Magnet Funnel
- Status: `HOLD`
- Why: Good compliance profile, but requires a sharper audience definition and distribution plan
- Notes: Must store acquisition source and proof of consent

### 5. Email List Brokerage or Contact Resale
- Status: `REJECTED`
- Why: Violates the compliance pack and depends on personal-data monetization
- Notes: Do not pursue or reactivate
