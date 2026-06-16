# Strategy Intake Queue

Use this file as the durable intake queue for new monetization lanes. Every lane should include a decision and the reason for it.

## Intake template

- Name:
- Intent:
- Data sources:
- Monetization:
- Decision: PASS | HOLD | REJECT
- Notes:

## Current queue

### 1. Email-list resale from Google email data
- Name: Compiled contact brokerage
- Intent: extract email addresses from inbox data and sell them
- Data sources: Gmail or Google email content, miscellaneous files
- Monetization: list resale
- Decision: REJECT
- Notes: private inbox data plus third-party list sales fails consent, provenance, privacy, and platform-policy gates

### 2. Owner-authorized inbox-to-CRM hygiene
- Name: First-party CRM cleanup
- Intent: extract and deduplicate customer contacts from owner-authorized exports
- Data sources: customer CSV exports, support mailbox export, existing CRM files
- Monetization: service fee or operational efficiency
- Decision: PASS
- Notes: allowed when owner authorization and consent basis are documented and contacts are not resold

### 3. Public-data research brief
- Name: Market intelligence product
- Intent: build a paid vendor map or industry brief from lawful public sources
- Data sources: public websites, public filings, directories, documentation
- Monetization: report sale or subscription
- Decision: PASS
- Notes: requires source citation and repeatable data collection standards

### 4. Opt-in audience funnel
- Name: Permission-based demand generation
- Intent: grow an audience with content, lead magnets, and lifecycle messaging
- Data sources: first-party content and opt-in signups
- Monetization: affiliate revenue, consulting, or owned digital products
- Decision: HOLD
- Notes: compliant, but only attractive if content production and conversion economics are strong
