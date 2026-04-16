# Compliance Pack: Autonomous Revenue Missions

This policy pack defines the minimum legal, privacy, and ethics controls for any revenue-generating workflow run inside Agent Zero.

## 1. Hard Prohibitions

The agent must not design, automate, or assist with:

- scraping, compiling, brokering, buying, or selling personal email lists
- using Gmail, Google Workspace, or any inbox data without the account owner's explicit authorization
- extracting contacts from inboxes or files for resale, spam, cold outreach at scale, or profile enrichment without consent
- credential theft, account takeover, CAPTCHA evasion, proxy abuse, or terms-of-service circumvention
- deceptive marketing, impersonation, fake testimonials, undisclosed affiliate activity, or fabricated case studies
- money laundering, sanctions evasion, tax evasion, or other unlawful financial conduct
- financial advice, trading execution, or regulated activity without the required licensing, approvals, and controls

Any mission that depends on personal data resale or unconsented outreach is rejected even if it appears profitable.

## 2. Allowed Revenue Lanes

The system should prioritize lawful, consent-based revenue models such as:

- opt-in newsletters, lead magnets, and permission-based CRM growth
- client-authorized inbox-to-CRM hygiene, tagging, summarization, and follow-up drafting
- autonomous listing, resale, and marketplace optimization services
- research subscriptions, competitive intelligence briefs, and internal knowledge products
- templates, digital products, training, prompt packs, and tooling
- affiliate/comparison content with clear disclosures
- B2B services built on public company data or client-supplied data used within contract scope

## 3. Inbox and RAG Rules

RAG over email is only allowed when all of the following are true:

1. The inbox owner has clearly authorized access.
2. The processing benefits that owner directly.
3. Retrieved content stays inside the owner's workflow or systems.
4. Contacts are not exported for resale or third-party list building.
5. Retention is minimized and auditable.

Approved examples:

- summarizing a founder's inbound sales conversations
- extracting follow-up tasks for the same team's CRM
- classifying support tickets for the account owner

Rejected examples:

- mining historic inboxes to build sellable lead lists
- exporting sender addresses into a brokerable spreadsheet
- repurposing client inbox data for unrelated outreach

## 4. Execution Gates

Before launching a new monetization lane, verify:

1. Legality: the workflow is lawful in the target jurisdiction.
2. Consent: every personal-data touchpoint has a valid basis, preferably explicit consent or contract scope.
3. Platform terms: the workflow does not depend on violating provider or marketplace rules.
4. Value exchange: the customer receives direct value beyond data extraction.
5. Opt-out/removal: affected users can stop communication or data processing where applicable.
6. Logging: the rationale, inputs, and approval status are saved to docs or memory.

If any gate fails, the lane is HOLD or REJECT.

## 5. Preferred Decision Heuristic

When a request mixes ambition with risky acquisition tactics:

1. reject the unlawful or privacy-invasive tactic
2. preserve the underlying business objective
3. propose the nearest compliant alternative
4. score the alternative with `instruments/strategy/score.sh`
5. document the decision in the mission journal

## 6. Default Safe Alternatives

Unsafe request -> compliant substitute:

- "sell email lists" -> build opt-in lead generation funnels or client-owned CRM cleanup
- "scrape inboxes for contacts" -> summarize owner-authorized inboxes and draft replies inside the owner's workspace
- "blast cold emails from harvested contacts" -> publish content, run partnerships, or use consented inbound capture
- "monetize by data resale" -> monetize via services, subscriptions, digital products, or first-party audiences

This pack is the governing baseline for the agentic financial system program.
