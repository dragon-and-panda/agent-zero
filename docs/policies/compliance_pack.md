# Compliance Pack for Autonomous Revenue Systems

This pack defines the minimum legal, privacy, and platform-compliance rules for any revenue-seeking workflow built with Agent Zero.

## 1. Non-negotiable guardrails

The agent must reject or halt any workflow that relies on:

- selling, renting, brokering, or trading personal email lists or contact databases
- compiling contact lists from Gmail, Google Workspace, inbox exports, or local files for resale
- scraping inboxes, mailboxes, or third-party systems without clear account-owner authorization
- spam, unsolicited bulk outreach, or outreach that bypasses consent requirements
- credential abuse, CAPTCHA evasion, identity spoofing, or platform-rule evasion
- collecting or storing personal data beyond a narrowly documented, user-authorized purpose

## 2. Allowed revenue lanes

The agent may pursue compliant alternatives such as:

- first-party CRM hygiene for a mailbox or dataset owned by the customer
- consent-based newsletter, community, or customer-list operations
- inbox triage, summarization, tagging, and support automation for the account owner
- autonomous listing, merchandising, and resale services for goods the customer owns
- research products, intelligence briefs, and software tools sold without personal-data resale
- lead generation based on public company information or explicit opt-in sources

## 3. Gmail and email-data policy

Gmail or email-derived data may only be processed when all of the following are true:

1. the mailbox owner or an authorized client has explicitly approved the workflow
2. the purpose is operational, analytical, or customer-service related
3. the output is limited to the owner's internal use, CRM hygiene, support operations, or consent-based outreach
4. provenance and consent are preserved in the resulting records

The following are expressly prohibited:

- turning inbox data into a list for sale
- extracting addresses from message histories for cold outreach
- enriching or merging inbox-derived contacts into a brokered dataset

## 4. Local analysis tools

Local analysis software, including Orange or similar data-mining tools, may only be used on:

- client-owned or first-party datasets
- datasets with documented consent or lawful business purpose
- sanitized datasets that do not exceed the minimum data needed for the job

They must not be used to organize or prepare personal contact lists for resale.

## 5. Decision gates before execution

Every monetization idea must be screened for:

- legality
- consent
- data provenance
- platform compliance
- business attractiveness

If legality, consent, provenance, or platform compliance are unclear, the workflow stays on HOLD or is REJECTED.

## 6. Canonical examples

### Reject

- "Export Gmail contacts, combine them with addresses from old files, and sell the list."
- "Scrape inbound leads from multiple inboxes and package them for brokers."

### Hold

- "Use a client's inbox to identify customer contacts for reactivation."
  - Hold until the client confirms account ownership, scope, consent posture, and intended channel rules.

### Pass

- "Clean and deduplicate an opt-in customer CSV, then sync consent-safe records into the client's CRM."
- "Run an autonomous marketplace listing service for items the client already owns."

## 7. Preferred fallback actions

When a request fails the guardrails, redirect the system toward one of these safer substitutes:

- first-party inbox-to-CRM hygiene
- consent-safe audience segmentation
- autonomous listing and resale operations
- research, content, or software products
- public-data market mapping without personal-data brokerage
