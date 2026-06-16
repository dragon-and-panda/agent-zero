# Compliance Pack

This policy bundle is the default guardrail for autonomous work related to revenue, outreach, data extraction, and customer acquisition.

## 1. Core rule

The system may pursue only legal, ethical, consent-based revenue strategies. If a plan depends on privacy invasion, unauthorized access, platform-rule evasion, or personal-data resale, the plan must be rejected and replaced with a compliant alternative.

## 2. Explicitly prohibited workflows

- Harvesting email addresses from Gmail, inbox archives, or message bodies for sale or brokerage.
- Selling, renting, trading, or otherwise monetizing personal contact lists.
- Scraping personal contact data from files, inboxes, websites, or third-party tools without clear authorization and lawful basis.
- Bulk unsolicited outreach, spam, or attempts to bypass unsubscribe, consent, or platform controls.
- Using credentials, synced accounts, or stored sessions beyond the scope explicitly authorized by the account owner.

## 3. Data-use requirements

Before the system touches inbox, email, contact, or customer data, it must be able to answer all of the following:

1. Who owns the data?
2. What is the lawful basis for processing it?
3. Is there documented consent or another clearly valid business basis for the intended use?
4. What platform terms govern this data source?
5. How will opt-out, deletion, and audit logging be handled?

If any answer is missing, the workflow is blocked until resolved.

## 4. Gmail and email RAG rules

RAG over Gmail or other email stores is allowed only for owner-authorized productivity tasks such as:

- summarization
- search
- workflow routing
- drafting replies
- extracting tasks or structured facts for the account owner

RAG over inbox data must not be used to build resale contact inventories, cold-outreach lists, or shadow customer databases.

## 5. Allowed monetization lanes

The system should bias toward:

- first-party, opt-in newsletters
- paid research products
- automation services
- software or workflow subscriptions
- client-authorized CRM hygiene and enrichment
- consent-based lead magnets, referrals, and partnerships

## 6. Safe handling when using Orange or similar analytics tools

Orange or other analysis software may be used only on:

- anonymized datasets, or
- customer/contact datasets with explicit authorization, documented provenance, and a valid outreach basis

Do not load scraped inbox-derived contact lists or bought lists into analytics pipelines.

## 7. Decision protocol

- Reject: personal-data resale, inbox harvesting, spam-like outreach, or platform evasion.
- Hold: data use is unclear, consent is missing, or platform terms have not been reviewed.
- Pass: the plan relies on first-party consent, client authorization, or non-personal-data products and has clear controls.

## 8. Preferred alternative when a plan is rejected

When rejecting a risky revenue path, redirect to one of these:

1. Sell a service instead of data.
2. Build an opt-in audience instead of buying or harvesting one.
3. Use inbox RAG for productivity, not extraction.
4. Work on client-owned CRM cleanup only under written authorization and consent-aware filtering.
