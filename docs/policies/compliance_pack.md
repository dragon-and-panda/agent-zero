# Compliance Pack for Autonomous Operations

This policy pack defines the minimum legal, privacy, and anti-abuse rules for autonomous workflows built with Agent Zero.

## 1. Non-negotiable prohibitions

Agents must not:

- access email, cloud accounts, files, or third-party systems without explicit authorization
- compile, buy, sell, lease, or otherwise monetize personal email lists or contact databases
- scrape or export personal data for spam, profiling, surveillance, or resale
- send unsolicited bulk outreach that violates platform terms or applicable law
- impersonate people or organizations, hide commercial intent, or use deceptive growth tactics
- exfiltrate credentials, secrets, tokens, invoices, payment data, or private conversations

## 2. Approved data sources

Agents may only use data that is:

- provided directly by the workspace owner
- stored in first-party systems the operator is authorized to access
- collected from users with clear consent for the stated purpose
- public and allowed to be used under the source platform's terms and local law

When processing data, agents should minimize collection, prefer summaries over raw exports, and retain only what is necessary for the task.

## 3. Gmail and RAG rules

RAG over email or documents is allowed only for legitimate first-party workflows such as:

- classifying support conversations
- extracting invoices, receipts, and renewal dates
- identifying tasks, opportunities, or follow-ups for the account owner
- organizing opted-in customer communications already lawfully collected

RAG over email or documents is not allowed for:

- harvesting addresses from mailboxes to build outbound lead lists
- inferring private relationships or sensitive attributes for monetization
- creating data products from personal correspondence
- reselling or sharing contact information with unrelated third parties

## 4. Data handling standards

- collect the minimum fields needed
- tag every dataset with source, owner, purpose, and retention window
- redact secrets and highly sensitive data before storage when possible
- prefer anonymized or aggregated analysis in Orange or similar tools
- avoid mixing unrelated datasets without a lawful documented reason

## 5. Outreach and growth rules

Any outbound growth workflow must use:

- consent-based lists, first-party CRM contacts, or clearly documented lawful-basis review
- accurate sender identity and commercial disclosure
- unsubscribe or opt-out handling where required
- throttling, logging, and complaint monitoring

Purchased lists, scraped contact lists, and hidden-recipient extraction are out of bounds.

## 6. Allowed monetization patterns

Preferred phase-1 revenue models include:

- productized services sold to inbound or referred prospects
- affiliate content and comparison research
- first-party newsletters with sponsorships or premium subscriptions
- internal automation tools sold as software or managed services
- anonymized market intelligence reports built from lawful non-personal data

## 7. Escalation rule

If legality, consent, privacy ownership, or platform terms are unclear, pause the workflow and request confirmation instead of proceeding.
