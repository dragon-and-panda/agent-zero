# Compliance Pack for Autonomous Revenue Workflows

This pack defines the non-negotiable rules for any Agent Zero workflow intended to generate revenue, handle user data, perform outreach, or integrate with third-party platforms.

It exists to keep autonomous programs effective **and** lawful. Revenue does not override privacy, consent, contract, or platform-policy obligations.

---

## 1. Core Principles

1. **Lawfulness first**
   - Do not build or run workflows that depend on illegal collection, misuse, resale, or processing of personal data.
   - Do not evade platform rules, rate limits, or anti-abuse controls.

2. **Consent and provenance**
   - Personal data must come from a source with documented authorization.
   - If consent, ownership, or allowed use is unclear, the workflow does not proceed.

3. **Purpose limitation**
   - Data collected for one purpose must not be repurposed for unrelated monetization.
   - Inbox access, CRM access, and file imports must stay within the user-approved scope.

4. **Least privilege**
   - Use the narrowest access possible for integrations, APIs, and internal roles.
   - Retain the minimum data needed for the approved workflow.

5. **Auditability**
   - Every monetization lane should have a written charter, scoring result, and journal trail.
   - Decisions that touch regulated or sensitive data must be explainable after the fact.

---

## 2. Prohibited Activities

The following are out of bounds for this repository and any agent operating from it:

- Scraping, compiling, enriching, brokering, or selling personal email lists.
- Extracting email addresses from Gmail, Google Workspace, or other inbox data for resale, lead dumping, or mass unsolicited outreach.
- Accessing inboxes, drives, CRMs, or messaging accounts without explicit authorization from the account owner.
- Building spam systems, bulk cold-outreach engines, or workflows primarily designed to bypass consent.
- Circumventing terms of service, CAPTCHAs, identity checks, or anti-bot controls where doing so would violate law or platform policy.
- Using deceptive identity, fabricated testimonials, fake business records, or impersonation to acquire revenue.
- Handling regulated data categories without a documented basis, scope, and control plan.

If a proposed lane requires any of the above to be viable, it must be rejected.

---

## 3. Allowed Revenue Patterns

These patterns are in scope when implemented with proper controls:

- **First-party workflow automation**
  - Example: an owner-authorized inbox assistant that classifies messages, drafts replies, and syncs opted-in contacts into a CRM.

- **Client-owned service delivery**
  - Example: automating listing creation, research, reporting, proposal generation, or customer support on behalf of a client that owns the source data.

- **Research, analytics, and decision support**
  - Example: market scanning, pricing analysis, productized research reports, internal forecasting, or operations dashboards.

- **Consent-based marketing operations**
  - Example: managing opt-in newsletter segments, lead scoring for existing contacts, or enrichment against customer-provided records where the use is contractually allowed.

- **Marketplace or platform services**
  - Example: listing optimization, catalog enrichment, buyer inquiry triage, scheduling, or inventory workflows that honor platform rules.

---

## 4. Data Access Rules

### 4.1 Inbox and Email Data

Email and inbox data may only be used when all of the following are true:

- The account owner has knowingly authorized the integration.
- The task is productivity, service delivery, or record management for that owner.
- The workflow does not export or repurpose contacts for resale or unsolicited bulk outreach.
- OAuth scopes are limited to what the approved workflow requires.
- Data retention and sync rules are documented.

### 4.2 Public Web Data

Public availability does **not** automatically make data fair game for collection or resale.

Before use, confirm:

- terms of service allow the access pattern,
- the target data is not personal data being repackaged in a harmful way,
- the collection method is proportionate,
- the downstream use is disclosed and defensible.

### 4.3 Customer and CRM Data

- Only process records the user or client lawfully controls.
- Keep provenance notes for imported lists, uploads, or synced records.
- Support deletion, correction, and suppression workflows where applicable.

---

## 5. Opportunity Gating

Every new monetization lane must be scored before activation.

### Hard gates

Each of these must score **high**:

- legality
- consent
- provenance
- tos

If any hard gate is below high, the lane is rejected.

### Soft factors

These determine whether a compliant lane is ready now:

- time
- margin
- repeatability
- automation
- defensibility

Use `instruments/strategy/score.sh` to classify the lane as:

- `PASS`: hard gates clear, no soft factor is low, and the lane is strong enough to run now.
- `HOLD`: compliant but not yet attractive or mature enough.
- `REJECT`: fails a hard gate.

---

## 6. Approved Direction for the Agentic Financial System

The original mission included selling compiled email lists and mining inbox data for monetization. That direction is rejected by this policy pack.

Approved replacement lanes:

1. **Inbox-to-CRM assistant**
   - Use owner-authorized email access for triage, extraction of opted-in business context, and CRM hygiene.
   - No list resale. No mass cold email.

2. **Autonomous listing and catalog services**
   - Build on the lawful service blueprint in `docs/autonomous_listing_service.md`.

3. **Research and productized intelligence**
   - Produce reports, watchlists, summaries, and decision-support assets sold as a service.

4. **Client-owned workflow automation**
   - Automate internal operations for businesses that provide their own data and approval.

---

## 7. Required Artifacts for New Lanes

Before a lane is considered active, create or update:

- `docs/strategy/incoming.md`
- `docs/programs/<program>/charter.md`
- `docs/programs/<program>/journal.md`
- `docs/programs/<program>/improvements.md`
- `instruments/strategy/score.md`
- `instruments/strategy/score.sh`

Optional but recommended:

- prompt persona updates,
- telemetry hooks,
- retention notes,
- integration-specific SOPs.

---

## 8. Escalation Rules

Pause and escalate the lane when:

- consent records are missing,
- data provenance is unclear,
- platform terms appear to prohibit the method,
- the workflow touches regulated or highly sensitive information,
- the only plausible path to monetization is spam, resale of personal data, or deceptive behavior.

When in doubt, default to `HOLD` or `REJECT`, not creative reinterpretation.
