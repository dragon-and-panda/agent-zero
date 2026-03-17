# Compliance Pack for Autonomous Revenue Programs

This policy bundle defines the non-negotiable rules for any monetization workflow built on top of Agent Zero.

## 1. Mission Boundary
The objective is to build a self-sustaining financial system through lawful, ethical, consent-based online ventures. Revenue quality matters as much as revenue quantity.

## 2. Explicitly Prohibited Activities
The following are out of bounds:
- Harvesting email addresses or other personal contact data from inboxes, CC fields, files, scraped datasets, or breached data for resale.
- Selling, renting, brokering, or packaging personal email lists.
- Sending deceptive, unsolicited, or policy-violating mass outreach.
- Scraping or automating platforms in ways that violate terms of service, privacy law, or anti-spam rules.
- Circumventing security controls, CAPTCHAs, rate limits, or access boundaries.
- Using private or regulated data without documented authorization.
- Operating payment or transfer workflows for accounts that are not owned and controlled by the project operator.

## 3. Approved Data Practices
Data work is allowed only when the source and use are compliant.

### Allowed
- Processing the operator's own email or documents for summarization, search, CRM hygiene, or task automation.
- Processing a client's inbox or CRM only with written authorization and a clear service purpose.
- Using public business information, first-party data, or explicit opt-in lists.
- Exporting only the minimum fields required to fulfill the service.
- Using Orange Data Mining or similar tools on consented or operator-owned datasets for segmentation, deduplication, and analysis.

### Not Allowed
- Converting third-party inbox content into lead lists for sale.
- Re-identifying pseudonymous data to discover personal contacts.
- Copying contact data into monetization workflows without consent logging.

## 4. Approved Revenue Tracks
Preferred tracks for this repo:
1. Consent-based inbox-to-CRM hygiene services for founders, agencies, and small teams.
2. Autonomous listing concierge services for marketplace sellers.
3. Course, tutorial, and content products documenting workflows, experiments, and operating playbooks.
4. Public-data market research briefs that summarize industries, competitors, and demand signals without trafficking in personal data.
5. Automation retainers where agents save operator or client time using authorized systems.

## 5. RAG Guardrails for Email and Documents
If RAG is applied to email or file corpora:
- The corpus must belong to the operator or an authorized client.
- Retrieval outputs should default to summaries, clusters, and workflow suggestions rather than raw bulk export of personal data.
- Personal data should be redacted or minimized in artifacts stored to `knowledge/`, `logs/`, or external systems.
- Any downstream CRM sync must preserve consent metadata.

## 6. Outreach and Sales Guardrails
- Outreach must be targeted, truthful, and relevant to a legitimate business purpose.
- Prefer warm intros, inbound capture, content funnels, or low-volume human-reviewed outbound.
- Do not auto-send messages that impersonate humans or conceal AI assistance when disclosure is required.
- Keep unsubscribe and opt-out handling documented.

## 7. Treasury and Risk Controls
This project is a business-building system first, not a speculative trading system.
- Maintain an operating reserve before allocating capital to higher-risk experiments.
- Treat leveraged forex or similar instruments as deferred research, not the primary monetization engine.
- If any trading sandbox is added later, require paper-trading validation, max-drawdown limits, and explicit stop conditions before live capital is used.
- Settlement destinations must comply with platform rules, tax rules, and the operator's own account controls.

## 8. Mandatory Documentation
Every monetization workflow must record:
- data source,
- legal basis / authorization,
- expected customer value,
- pricing model,
- downside risks,
- fallback plan,
- metrics used to decide continue / pause / kill.

## 9. Stop Conditions
Pause the workflow immediately if any of the following occur:
- unclear authorization to access data,
- evidence of privacy or anti-spam risk,
- customer complaints about deceptive outreach,
- payment account restrictions,
- repeated platform policy violations,
- inability to explain the workflow in plain language to a customer or regulator.

## 10. Default Rule
When speed conflicts with legality, privacy, or honesty, choose the compliant path or do not proceed.
