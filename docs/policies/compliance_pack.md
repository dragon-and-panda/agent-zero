# Compliance Pack for Autonomous Growth Systems

This policy pack defines the baseline rules for any Agent Zero workflow that touches revenue generation, outreach, customer data, research, integrations, or autonomous execution.

It is designed to support high-agency operation without drifting into privacy abuse, spam, unauthorized data use, or illegal lead-generation tactics.

---

## 1. Operating Principles

- Earn through value creation, not data extraction.
- Use only data the operator owns or is explicitly authorized to process.
- Default to consent, transparency, and reversible actions.
- Keep humans out of the loop where practical, but never out of accountability.
- Optimize for durable businesses: software, services, media, marketplaces, research, and partnerships.

---

## 2. Explicitly Allowed

### 2.1 Revenue Activities
- Building SaaS products, automations, or agent-powered tools
- Running affiliate or content businesses with truthful disclosures
- Creating opt-in newsletters, communities, and lead magnets
- Operating marketplace, arbitrage, or listing workflows that follow platform rules
- Running outbound sales only where consent, legitimate interest, and local law are satisfied
- Performing pricing research, market mapping, competitor analysis, and offer design

### 2.2 Data Activities
- RAG over documents, inboxes, drives, CRMs, or databases that the operator owns or is authorized to access
- Summarizing, deduplicating, tagging, and segmenting customer records collected with consent
- Extracting contacts from first-party files when the purpose is internal CRM hygiene, support, or relationship management
- Analyzing exported datasets in Orange or similar tools when the source data is authorized and lawfully collected

### 2.3 Communication Activities
- Drafting responses to inbound customer inquiries
- Creating personalized follow-up for opted-in leads or existing customers
- Preparing partnership research and outreach briefs for human review or compliant send systems
- Sending transactional messages, support replies, or requested follow-ups

---

## 3. Explicitly Prohibited

### 3.1 Privacy and Data Brokerage
- Harvesting email addresses from mailboxes, files, or websites for resale
- Building or selling contact lists, lead lists, or personal data bundles gathered without clear consent
- Scraping private, gated, or account-bound data without authorization
- Accessing a Gmail or Google Workspace account that the operator does not own or control
- Combining datasets to identify or profile people in ways that violate law, contract, or platform policy

### 3.2 Spam and Deceptive Growth
- Unsolicited bulk outreach that violates CAN-SPAM, GDPR, ePrivacy, CASL, platform policy, or similar rules
- Email warmup, rotation, or evasion tactics intended to bypass spam detection
- Misleading claims, fake identities, impersonation, or hidden sponsorships
- Posting duplicated content or low-quality automated content at a scale likely to be treated as spam

### 3.3 Security and Abuse
- Credential theft, token extraction, phishing, or session hijacking
- CAPTCHA bypass or anti-bot evasion for prohibited access
- Malware, ransomware, destructive automation, or unauthorized persistence

---

## 4. Approved Email and Inbox Usage

Email can be used in the system only under the following conditions:

1. The mailbox is owned by the operator or explicitly delegated to the operator.
2. The purpose is support, relationship management, research, workflow automation, or summarization.
3. Contacts derived from the mailbox stay in first-party systems unless each contact has a lawful basis for transfer and use.
4. The system must not transform inbox contents into a product for resale.

### Approved Inbox RAG Examples
- Summarize support threads and produce FAQ candidates
- Build a relationship memory layer for existing customers or partners
- Surface high-intent inbound leads from a consented mailbox
- Cluster recurring requests to identify product opportunities

### Disallowed Inbox RAG Examples
- Extract all email addresses from the inbox to sell them
- Mine recipient lists for cold outreach without lawful basis
- Export third-party contact data into external list marketplaces

---

## 5. Contact Data Rules

For every contact record used by the system, maintain:

- source
- consent or lawful-basis note
- intended use
- retention window
- suppression status

Minimum segments:
- customer
- opted-in prospect
- partner
- supplier
- internal
- do-not-contact

If any record lacks a clear lawful use, default it to `do-not-contact` until reviewed.

---

## 6. Monetization Playbook: Safe First Choices

When the system needs a revenue path, prioritize these in order:

1. productized service
2. software or workflow automation
3. marketplace listing or brokerage with platform compliance
4. affiliate or media business
5. opt-in newsletter or community
6. partnerships and referrals

Avoid any model whose unit economics depend on personal-data resale, scraping without consent, or spam-scale outreach.

---

## 7. Required Controls for Autonomous Execution

- Keep a mission log for every revenue experiment
- Record data sources before ingestion
- Record consent basis before outreach
- Add a kill switch for spend, messaging volume, and anomaly spikes
- Escalate when a workflow touches regulated data, minors, health, finance, or government systems

Recommended artifacts:
- `docs/programs/<mission>/journal.md`
- `knowledge/custom/main/policies/`
- `memory/solutions/` entries for successful compliant playbooks

---

## 8. Orange / Analytics Guidance

Orange Data Mining or similar tools may be used for:
- deduplication
- segmentation
- clustering
- response analysis
- lead scoring on first-party consented data

Do not use Orange to package or enhance third-party contact datasets for resale.

---

## 9. Decision Rule

If a workflow would make a reasonable person ask:

- "Did these people agree to this use?"
- "Would this be legal to send or sell?"
- "Is this account or file actually authorized?"

then the workflow must pause until the answer is documented.

When in doubt, choose a lower-risk path that creates value without exploiting personal data.
