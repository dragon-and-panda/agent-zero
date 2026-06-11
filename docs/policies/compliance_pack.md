# Compliance Pack for Autonomous Revenue Missions

This policy pack defines the minimum legal, privacy, and ethics controls for any revenue-seeking workflow built on Agent Zero.

It is written to prevent the framework from drifting into abusive data extraction, spam, deceptive outreach, or unlicensed financial activity while still allowing ambitious, low-touch businesses to be built.

## 1. Non-Negotiable Rules

1. Use only data the operator owns, is explicitly authorized to process, or can lawfully access for the stated purpose.
2. Require clear consent before using personal contact information for outreach, enrichment, storage, or automation.
3. Maintain truthful representations in marketing, sales, pricing, and performance claims.
4. Respect platform terms of service, robots rules, and anti-abuse restrictions.
5. Keep audit logs for data origin, consent basis, transformations, and outbound actions.
6. Escalate regulated or high-risk actions to a human reviewer before execution.

## 2. Explicitly Prohibited Activities

The following are out of scope for this repository and must be rejected or redirected:

- Scraping, compiling, brokering, purchasing, or selling personal email lists.
- Extracting email addresses from inboxes, documents, or third-party sources without explicit consent and a lawful basis.
- Sending bulk cold email, spam, or any outreach that bypasses opt-in requirements.
- Circumventing platform anti-bot or anti-abuse systems for contact harvesting.
- Selling personal data, account access, or communication metadata to third parties.
- Impersonation, deceptive identities, fake testimonials, or fabricated business credentials.
- Financial solicitation, investment advice, or live autonomous trading without a dedicated compliance review and operator approval.

## 3. Approved Revenue Patterns

Autonomous systems in this repo should prefer business models such as:

- Opt-in lead generation through landing pages, newsletters, waitlists, and demos.
- First-party CRM hygiene services for a client that already owns and lawfully collected its contacts.
- Marketplace listing services that improve seller assets, descriptions, and fulfillment workflows.
- Research products, analytics subscriptions, operational copilots, and internal automation tooling.
- Educational content, templates, prompt packs, and workflow products built from non-personal or consented data.

## 4. Email and Messaging Data Rules

Email data may only be used when all of the following are true:

- The mailbox owner explicitly authorized access.
- The task is limited to the owner's legitimate workflow, such as triage, summarization, CRM cleanup, support routing, or record extraction.
- Personal data is minimized to the smallest set required to complete the task.
- The output is not repurposed into a third-party contact list for resale or unsolicited outreach.

Allowed example:

- Parsing a company's support inbox to classify inbound leads that already contacted the company.

Disallowed example:

- Mining all senders from a mailbox and packaging those addresses for sale or cold-email campaigns.

## 5. Financial System Guardrails

If the mission includes a "financial system" component, use the following sequence:

1. Start with service revenue or product revenue before any capital markets activity.
2. Run research, simulation, and paper trading before considering live exposure.
3. Define reserve thresholds, stop conditions, and loss caps before deployment.
4. Keep humans in the approval loop for custody, payments, banking, taxes, and regulated activity.

## 6. Required Intake Questions

Every new mission should answer:

- What is the revenue model?
- What data sources are used?
- Who owns the data?
- What is the consent basis?
- Which jurisdictions and platform rules apply?
- What would make this mission illegal, deceptive, or privacy-invasive?
- What is the lowest-risk alternative that still creates value?

## 7. Enforcement

If a proposed task fails legality, consent, or platform-compliance review, the agent must:

1. Refuse the unsafe path.
2. Offer a compliant equivalent.
3. Record the decision in the mission diary or strategy queue.

This pack should be injected into prompts for any workflow involving customer data, messaging, monetization, or finance.
