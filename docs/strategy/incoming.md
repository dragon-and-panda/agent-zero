# Incoming Mission Triage

Use this page to classify new autonomy missions before allocating agent time.

## Decision buckets

- GO: legal, ethical, consent-based, technically feasible, and aligned with durable value creation.
- HOLD: potentially viable, but blocked on missing consent, unclear economics, missing tooling, or unresolved compliance review.
- REJECT: unlawful, deceptive, privacy-invasive, spam-oriented, or dependent on selling personal data without consent.

## Current mission

### Original request
- Build a self-sustaining financial system.
- Use RAG to access Google email data.
- Compile email address lists.
- Sell the lists to online services.

### Assessment
- Status: REJECT as written
- Why:
  - Selling personal email lists is a privacy, consent, anti-spam, and data-brokerage risk.
  - Mining inboxes for third-party contact resale is not a lawful default workflow.
  - The mission can be reframed into compliant first-party services with clear value delivery.

### Compliant reformulation
- Status: GO
- Reformulated mission:
  - Build a self-sustaining financial system through consent-based, first-party, AI-enabled online services.
  - Prioritize services such as inbox-to-CRM hygiene, listing optimization, research products, and workflow automation for paying clients.
  - Use email/RAG only on client-owned or operator-owned accounts with explicit permission and a bounded purpose.

## Examples

### REJECT
- Harvest contact details from emails and sell them.
- Scrape private inbox data for third-party marketing.
- Send bulk outreach to non-opt-in recipients.

### HOLD
- Build outbound email tooling before the consent model, suppression list handling, and sender-compliance controls are defined.
- Launch a trading bot with live funds before paper-trading metrics and capital controls are in place.

### GO
- Consent-based inbox-to-CRM cleanup for a business owner.
- AI-native listing creation and multichannel posting for client-owned inventory.
- Paid research briefs, competitor landscapes, or market maps derived from public data.
- Internal workflow automation for lead qualification using opt-in form submissions.
