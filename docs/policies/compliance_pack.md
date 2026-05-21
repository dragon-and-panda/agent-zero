# Compliance Pack: Agentic Financial System

This pack defines the non-negotiable rules for any autonomous revenue, research, outreach, or data workflow in this repository.

## 1. Core rule

The system may only pursue revenue through ethical, legal, consent-based, and platform-compliant means.

If a workflow depends on privacy abuse, credential misuse, deceptive behavior, spam, personal-data brokerage, or unauthorized access, the workflow must be rejected and replaced with a compliant alternative.

## 2. Explicitly prohibited

- Extracting email addresses, contact lists, or inbox data for sale, rental, exchange, or brokerage.
- Building or monetizing scraped personal-contact databases from Gmail, Google Workspace, uploaded files, exports, or third-party data dumps.
- Selling "lead lists", "contact lists", or similar personal data to online services or brokers.
- Sending spam, cold-email blasts, or unsolicited bulk outreach to scraped or purchased contacts.
- Accessing inboxes, drives, or accounts without clear authorization from the account owner.
- Using credentials, cookies, tokens, or browser sessions obtained without permission.
- Misrepresenting identity, business intent, or relationship status to obtain money, data, or access.
- Violating marketplace, ad-network, app-store, or API platform rules to create revenue.

## 3. Email and inbox data policy

RAG or analysis over email data is only allowed when all of the following are true:

1. The account is owned by the operator or the operator has explicit authority to process it.
2. The workflow is limited to a legitimate first-party purpose such as support, billing, knowledge extraction, CRM hygiene, or opportunity triage.
3. Only the minimum necessary data is processed and retained.
4. Contact details are not repackaged for resale, bulk outreach, or third-party transfer.

Allowed examples:

- Summarizing customer conversations from a first-party support inbox.
- Extracting invoice, refund, or renewal events from an owned mailbox.
- Identifying warm inbound partnership requests from messages already sent to the business.
- Building internal retrieval over the team's own operational correspondence.

Rejected examples:

- Export Gmail contacts and sell the addresses.
- Mine uploaded files for emails and package them into a list for buyers.
- Scrape inbox conversations to create third-party prospect databases.

## 4. Data-source tiers

### Green: preferred

- First-party business data collected directly from customers or users with notice.
- Double opt-in subscribers.
- Public business information intended for discovery, where use still complies with platform rules and applicable law.
- Internal operational records with a clear business purpose.

### Yellow: review required

- Public-web prospect research that may trigger outreach or platform-policy issues.
- Partner-provided datasets that require contractual review.
- Mixed datasets that contain both operational data and personal contact fields.

### Red: reject

- Purchased personal-data lists.
- Scraped personal email databases.
- Inbox exports intended for resale or unsolicited mass outreach.
- Data with unclear ownership, consent, or provenance.

## 5. Approved revenue patterns

Preferred phase-1 revenue lanes:

- Productized services with clear customer value.
- Marketplace listing automation for owned or authorized inventory.
- Digital products, templates, and research products built from original work.
- Affiliate or referral programs that comply with the host platform and disclosure rules.
- First-party lead capture funnels using opt-in forms, newsletters, demos, or waitlists.
- Compliant inbound-opportunity triage from the business's own inbox or CRM.

## 6. Required decision gates

Before launching a new monetization workflow, confirm:

- Legal basis is clear.
- Data provenance is documented.
- Consent and permissions are adequate.
- Platform terms are not being bypassed.
- The value proposition does not depend on privacy abuse or spam.

If any gate fails, the workflow must return HOLD or REJECT and propose a safer substitute.

## 7. Orange DataScaping or similar tooling

Orange DataScaping, spreadsheet mining, clustering, and enrichment tools may be used only on:

- first-party datasets,
- explicit opt-in contact lists,
- public business records used within applicable rules, or
- internal operating data.

They may not be used to industrialize personal-email harvesting, inbox scraping for resale, or contact-list brokerage.
