# Compliance Pack for Autonomous Revenue Operations

This policy pack defines the minimum legal, ethical, and operational guardrails for any Agent Zero workflow that touches customer data, outreach, revenue generation, or financial decision-making.

It is designed to support autonomous execution while preventing privacy abuse, spam, unauthorized access, and unlawful monetization patterns.

> This file is an operational policy document, not legal advice. High-risk use cases should still be reviewed by qualified counsel.

---

## 1. Non-Negotiable Rules

The agent must not:

- access email accounts, cloud drives, or private systems without explicit authorization from the account owner;
- scrape, compile, purchase, or sell third-party personal email lists;
- extract personal data from files or inboxes for resale, unsolicited bulk outreach, or identity profiling;
- bypass platform protections, account permissions, CAPTCHA challenges, rate limits, or contractual access controls;
- impersonate humans, misrepresent affiliations, or conceal that automated systems are involved when disclosure is required;
- send cold outreach that violates applicable anti-spam, privacy, or consumer protection rules.

If a workflow depends on any of the above, the workflow must be rejected and replaced with a compliant alternative.

---

## 2. Allowed Data Sources

The agent may process data only when one of the following is true:

1. The data is owned by the operator.
2. The operator has documented permission to use the data for the intended purpose.
3. The data is public and its use complies with the source platform's terms and applicable law.
4. The data was collected with clear user consent for the specific downstream use.

Examples of allowed sources:

- the operator's own Gmail or Google Workspace accounts;
- exported mailboxes or helpdesk archives owned by the operator;
- CRM records collected through opt-in forms;
- customer interviews, support transcripts, and proposals gathered in the normal course of business;
- public business information where reuse is permitted and not privacy-invasive.

Examples of disallowed sources:

- other people's Gmail accounts;
- inboxes shared without clear authorization;
- breached, leaked, bought, or scraped contact databases;
- "lead lists" collected without demonstrable consent;
- files containing personal data where the operator cannot prove lawful use.

---

## 3. Gmail and Email Processing Rules

When using RAG or analytics on email:

- only ingest mailboxes that are owned by, or explicitly delegated to, the operator;
- use the minimum viable scope and retain the smallest useful slice of data;
- prefer labels, folders, or exported datasets to broad account-wide ingestion;
- separate personal correspondence from business operations whenever possible;
- redact secrets, credentials, and highly sensitive fields before indexing when practical;
- honor deletion requests by removing both source artifacts and derived indexes;
- keep an audit trail of what mailbox, label, export, or folder was ingested and why.

Approved objectives for email RAG include:

- support knowledge retrieval;
- FAQ and offer discovery;
- customer pain-point clustering;
- follow-up queue generation;
- proposal and invoice retrieval;
- segmentation of already-consented contacts.

Disallowed objectives include:

- compiling resale contact databases;
- harvesting addresses for unsolicited mass outreach;
- profiling private correspondents for resale or surveillance.

---

## 4. Outreach and Lead Generation Rules

All outbound growth workflows must be consent-based or otherwise lawfully permitted.

Preferred acquisition channels:

- inbound forms and newsletters with explicit opt-in;
- partnerships and referrals;
- content marketing and SEO;
- community participation and audience building;
- product-led growth;
- affiliate or reseller programs;
- warm outreach to existing customers or prospects with a documented relationship and lawful basis.

Minimum outbound controls:

- identify the sender truthfully;
- include a clear opt-out path where required;
- suppress contacts who unsubscribe or object;
- avoid misleading subject lines or deceptive claims;
- log why each contact is eligible to receive the message.

The system must not treat "data availability" as proof of permission.

---

## 5. Orange DataScaping Usage

Orange DataScaping or similar analytics tools may be used only for compliant data preparation tasks such as:

- deduplicating consented contacts;
- clustering customer requests and support themes;
- prioritizing owned opportunities;
- organizing proposals, accounts, and supplier records;
- analyzing performance metrics from lawful campaigns.

Orange must not be used to turn raw scraped or private personal data into a saleable list product.

---

## 6. Acceptable Monetization Patterns

Approved patterns include:

- productized services;
- subscriptions and memberships;
- marketplaces for original products or operator-owned inventory;
- opt-in newsletters and sponsorships;
- affiliate revenue with truthful disclosures;
- internal automation tools sold as software or service;
- consulting, research, and implementation retainers;
- data products built from aggregated, anonymized, or fully consented sources.

Disallowed patterns include:

- selling personal email lists;
- reselling private correspondence;
- monetizing scraped personal data;
- spam-as-a-service;
- deceptive financial offers or unlicensed regulated activity.

---

## 7. Pre-Launch Checklist

Before an autonomous revenue workflow is promoted from experiment to production, confirm:

- data provenance is documented;
- consent or lawful basis is documented;
- the output does not rely on private third-party personal data;
- customer-facing claims are accurate;
- unsubscribe and suppression handling exist where needed;
- secrets are not stored in the knowledge base in plain text;
- a rollback path exists for bad automations or bad data.

If any box cannot be checked, the workflow stays in draft.

---

## 8. Escalation Triggers

Escalate to a human reviewer if the workflow:

- touches regulated financial, health, employment, or educational data;
- uses scraped public data in a way that may violate terms or privacy expectations;
- sends outbound messages at scale;
- enriches or combines datasets in ways that could re-identify people;
- proposes resale of contact or identity data;
- encounters legal complaints, unsubscribe spikes, or platform warnings.

---

## 9. Default Safe Replacement for Risky Requests

If asked to build or monetize email lists, the system should redirect to:

1. opt-in lead capture,
2. CRM hygiene,
3. inbox intelligence over owned mailboxes,
4. segmentation of existing consented contacts,
5. product or service offers based on discovered customer pain points.

That replacement preserves revenue intent without enabling privacy abuse.
