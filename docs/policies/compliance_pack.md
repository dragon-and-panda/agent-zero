# Compliance Pack for Autonomous Revenue Workflows

This policy pack defines the minimum legal, privacy, and platform-safety rules for any revenue-generating workflow built on Agent Zero.

## 1. Non-Negotiable Boundaries

The system must not:

- scrape, compile, broker, or sell personal email lists;
- extract contact details from inboxes, files, or websites for resale;
- bypass access controls, account permissions, rate limits, or platform terms;
- use stolen, leaked, purchased, or unclear-provenance personal data;
- automate spam, phishing, impersonation, or deceptive outreach;
- make regulated financial claims without qualified human review.

Any workflow that depends on those behaviors is out of scope and must be rejected or redesigned.

## 2. Approved Data Patterns

Allowed patterns are limited to:

1. **First-party data**  
   Data the operator already owns or lawfully controls, such as their own inbox, CRM, help desk, or uploaded files.

2. **Explicitly opted-in contacts**  
   Contacts who knowingly consented to receive communications for the relevant purpose.

3. **Client-owned data with authorization**  
   Data processed on behalf of a client who has rights to the data and has instructed the operator to use it.

4. **Public business information with clear provenance**  
   Only when collection and use are consistent with the source platform's terms and the intended use is lawful in the target jurisdiction.

If provenance, consent, or terms-of-service status is unclear, the workflow must be placed on hold.

## 3. Gmail / Email RAG Rules

RAG over email is allowed only under the following constraints:

- access must be limited to the mailbox owner or an authorized client mailbox;
- retrieval should be query-time and task-scoped, not bulk export by default;
- the system should summarize or classify messages instead of mass-copying raw content;
- address extraction must be limited to user-approved operational purposes, such as CRM sync, deduplication, support routing, or invoicing;
- bulk export of email addresses for resale, list trading, or indiscriminate cold outreach is prohibited;
- retention must be minimized, with deletion and audit controls documented.

## 4. Outreach and Growth Rules

Allowed growth systems should prefer:

- inbound lead capture;
- referral systems;
- opt-in newsletters;
- client-approved sales pipelines;
- account-based follow-up to existing relationships.

Cold outreach automation must not be enabled unless the operator separately verifies jurisdictional requirements, suppression handling, identity disclosures, and platform policy compliance.

## 5. Required Gating Checklist

Every new monetization lane must be scored on:

- legality;
- consent quality;
- data provenance;
- terms-of-service compatibility;
- automation fit;
- time-to-cash;
- differentiation;
- operational burden.

Reject the lane immediately if legality, consent, provenance, or terms-of-service compatibility is low.

## 6. Preferred Monetization Lanes

The current preferred lanes for this program are:

1. **Inbox-to-CRM assistant**  
   Turn user-owned email into structured opportunities, follow-up tasks, and CRM records.

2. **Autonomous listing and optimization services**  
   Use the existing listing-service work as a compliant, service-based revenue lane.

3. **Research and intelligence products**  
   Produce paid reports, watchlists, and workflow templates from lawful sources.

4. **Client-owned workflow automation**  
   Build automations for support, sales operations, procurement, and vendor management using client-authorized data.

## 7. Operational Controls

- Keep a mission diary for decisions and compliance assumptions.
- Record provenance for every imported data source.
- Use data minimization by default.
- Require human sign-off before activating any lane that touches regulated domains, financial transactions, or mass communications.
- Prefer service revenue, subscriptions, and software enablement over brokerage of personal data.

## 8. Example Decisions

### Reject
- "Compile email addresses from Gmail and other files, then sell the list."
- "Scrape public profiles to build a cold-email database."
- "Use RAG to harvest contacts from old mailboxes for monetization."

### Hold
- "Collect business contacts from a platform with unclear API and unclear terms."
- "Launch bulk outbound email before suppression and consent handling are in place."

### Pass
- "Analyze my own inbox and create a CRM of inbound leads."
- "Summarize vendor and customer conversations from an authorized mailbox."
- "Sell a workflow product that helps clients organize their own first-party communications."
