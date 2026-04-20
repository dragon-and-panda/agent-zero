# Compliance Pack for Autonomous Revenue Programs

This policy bundle defines the minimum guardrails for any autonomous monetization workflow inside Agent Zero.

## Hard prohibitions

- Do not scrape, extract, broker, or sell personal email addresses, contact lists, or other personal data.
- Do not access inboxes, contact stores, or cloud accounts without clear customer authorization and a legitimate business purpose.
- Do not automate spam, cold outreach without consent, CAPTCHA evasion, rate-limit evasion, account farming, or deceptive platform behavior.
- Do not monetize third-party data that lacks a clear license, contract, or first-party consent basis.

## Required pre-launch checks

Every new revenue workflow must answer all of the following before activation:

1. Legal basis
   - Is the activity lawful in the operating jurisdictions?
   - Are privacy, consumer-protection, and platform-specific rules satisfied?
2. Data provenance
   - Is each dataset public, licensed, customer-owned, or first-party?
   - Can the source and permitted use be documented?
3. Consent and authorization
   - If customer data is involved, is there clear user or client authorization?
   - Is the workflow limited to the authorized business purpose?
4. Platform compliance
   - Do the target platforms allow the automation?
   - Does the workflow avoid evasion, impersonation, or anti-abuse violations?
5. Auditability
   - Can the agent explain what data it used, why it used it, and what outputs it produced?

## Approved monetization lanes

Use these patterns instead of personal-data brokerage:

- Client-owned inbox-to-CRM services
  - Triage, classify, summarize, and draft replies for a client's own support or sales inbox.
  - Keep extracted data inside the client's CRM or helpdesk.
- Productized marketplace services
  - Listing creation, merchandising, repricing, and support workflows for client-owned inventory.
- Research and intelligence products
  - Reports, benchmarks, dashboards, and subscriptions built from public, licensed, or first-party data.
- Opt-in audience building
  - Newsletters, lead magnets, webinars, and referral programs where contacts explicitly opt in.

## Escalation rules

- Reject the workflow immediately if it depends on selling contact lists, scraping inboxes for resale, or bypassing platform protections.
- Hold the workflow if consent, provenance, or platform-permission details are missing.
- Approve only when the workflow has a lawful basis, auditable data provenance, explicit authorization where needed, and a platform-compliant execution plan.
