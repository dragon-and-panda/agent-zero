# Compliance Pack for Agentic Revenue Programs

This pack defines the hard constraints for any autonomous or semi-autonomous revenue program built in this repository.

## 1. Non-Negotiable Rules

- Do not scrape, buy, broker, package, or sell personal email lists.
- Do not extract contacts from inboxes, files, or SaaS systems unless the account owner has explicitly authorized that exact use.
- Do not use Gmail, Google Workspace, or other mailbox data to build third-party marketing lists.
- Do not send spam or automate outreach to people who have not opted in or who lack another lawful basis for contact.
- Do not misrepresent consent, source, or ownership of personal data.
- Do not automate account creation, anti-bot evasion, CAPTCHA defeat, or platform abuse for growth.
- Do not launch speculative financial trading or wagering loops with real money until they have passed explicit simulation, risk, and reserve gates.

## 2. Allowed Data Uses

Data use is allowed only when all of the following are true:

1. The data subject or account owner has granted clear permission.
2. The purpose is narrow, documented, and consistent with the permission granted.
3. The workflow uses the minimum data necessary.
4. Outputs stay under the control of the owner or an authorized operator.
5. Deletion, audit, and export paths exist.

Examples of allowed uses:

- Inbox-to-CRM hygiene for a business using its own Google Workspace account.
- Summarizing support email trends for the mailbox owner.
- Deduplicating and tagging first-party contacts that were already collected with consent.
- Building internal research dashboards from company-owned documents and approved exports.

Examples of disallowed uses:

- Harvesting addresses from inboxes or files for resale.
- Compiling cold-email targets from mixed personal datasets with unclear consent.
- Using RAG over private mailboxes to discover leads for third-party sale.
- Offering "done-for-you" contact list generation sourced from personal or scraped data.

## 3. Revenue Lanes That Pass This Pack

Prefer these revenue lanes:

- Consent-based Inbox-to-CRM Hygiene Service
- Autonomous Listing and resale services for client-owned inventory
- First-party lead qualification and CRM enrichment
- Research briefs, market maps, and internal intelligence products
- Content, templates, and automation packs for operators
- Back-office workflow automation for clients using their own systems and data

## 4. Revenue Lanes That Fail This Pack

Reject these lanes:

- Personal email list brokerage
- Inbox scraping for list resale
- Unconsented cold outreach at scale
- Identity/data brokerage
- Growth tactics that rely on platform evasion or impersonation

## 5. Required Gates Before Activation

Every new revenue lane must pass:

### Legality Gate
- A documented lawful use case exists.
- Terms of service and platform rules are not being bypassed.

### Consent Gate
- Consent or authorization is explicit and provable.
- The data destination and purpose match the consent scope.

### Operational Gate
- There is a human-review path for exceptions.
- Audit logs can explain what the system accessed and produced.

### Unit Economics Gate
- The lane can be tested with a small first-party dataset or simulation.
- Time-to-cash, margin, and repeatability are measurable.

## 6. Google Email / RAG Specific Rules

If a workflow touches Gmail or Google Workspace:

- Only use APIs, exports, or tokens supplied by the verified account owner.
- Request the smallest possible scope.
- Default to read-only unless a write action is necessary and approved.
- Keep outputs inside owner-controlled systems such as a CRM, ticketing tool, or internal report.
- Never transform mailbox data into a brokered lead asset.

## 7. Orange DataScaping Use

Orange DataScaping or similar tooling may be used only for:

- analyzing first-party, consented datasets
- clustering inbound customer inquiries
- segmenting approved CRM exports
- ranking revenue opportunities from compliant data

It must not be used to launder or organize unlawfully gathered contact data.

## 8. Trading and High-Risk Finance Guardrail

If the broader financial system later evaluates trading or wagering ideas:

- start with paper trading or simulation only
- require explicit bankroll and drawdown rules
- require logging of win rate, variance, and stop conditions
- do not move to live capital without objective evidence and human sign-off

## 9. Default Redirect

When an incoming mission fails legality or consent review, redirect it into one of these alternatives:

- opt-in newsletter growth
- first-party CRM cleanup and routing
- inbound lead scoring
- research and intelligence reports
- inventory listing and resale automation
- client-owned workflow automation
