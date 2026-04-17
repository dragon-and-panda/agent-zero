# Compliance Pack

This policy pack defines the minimum operating rules for autonomous workflows that touch user data, communications, growth, or monetization.

## 1. Core principles
- Operate lawfully and transparently.
- Use the least data and access needed to complete the task.
- Respect consent, privacy, platform terms, and reasonable user expectations.
- Prefer reversible, auditable actions over opaque automation.

## 2. Explicitly prohibited uses
Do not use Agent Zero workflows to:
- harvest email addresses or other personal contact details from inboxes, files, websites, or third-party systems for resale or cold outreach
- compile, enrich, broker, buy, or sell personal data without a lawful basis and explicit consent where required
- send spam or generate mass unsolicited outreach
- bypass authentication, rate limits, CAPTCHAs, paywalls, or service protections
- exfiltrate confidential information, credentials, tokens, or customer data
- access mailboxes or accounts without clear authorization from the account owner

## 3. Gmail and message-data rules
Gmail, IMAP, exported mail, and other message stores may only be used when all of the following are true:
1. The mailbox owner or authorized administrator has granted access.
2. The task is directly related to that owner's legitimate business purpose.
3. Retrieved data is limited to the minimum needed for the task.
4. Message content is not repurposed into lead lists, data brokerage assets, or unrelated marketing datasets.

Allowed examples:
- inbox triage
- support classification
- summarization for the mailbox owner
- retrieval over the owner's own correspondence to answer questions

Disallowed examples:
- extracting every sender email into a sellable list
- building prospect databases from private inbox history
- sharing correspondents' personal details with third parties

## 4. Outreach and marketing rules
Allowed growth workflows should be based on:
- explicit opt-in forms
- customer-requested follow-up
- existing contractual relationships
- public company information used for account research, not personal-data resale
- marketplace listings, affiliate content, digital products, and productized services

Before enabling outreach automation, document:
- who collected the contact data
- when and how consent was obtained
- what retention period applies
- how recipients can opt out

## 5. Data handling controls
- Store only fields required for the task.
- Tag records with source, consent status, and retention notes.
- Separate public business facts from personal contact data.
- Delete temporary exports when no longer required.
- Avoid copying sensitive datasets into prompts when metadata or summaries are enough.

## 6. Monetization guidance
Prefer these monetization models over personal-data brokerage:
- subscription software
- internal ops automation for paying clients
- digital products, templates, and reports
- affiliate or referral programs
- content-driven lead generation with opt-in capture
- marketplace services using platform-approved customer acquisition flows

## 7. Decision rule
If a task would surprise the data subject, violate platform terms, create unwanted outreach, or depend on non-consensual personal-data extraction, stop and redesign the workflow around consent-based inputs or non-personal data.
