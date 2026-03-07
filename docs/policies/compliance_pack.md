# Compliance Pack: Agentic Financial System

This policy pack is mandatory for all workflows in the Agentic Financial System program.

## 1) Non-Negotiable Rules

1. Do not collect, process, or sell personal data without a lawful basis and explicit consent where required.
2. Do not build or distribute scraped email lists for third-party sale.
3. Do not access accounts, inboxes, or files that are not owned/authorized by the operator.
4. Do not run deceptive marketing, impersonation, spam, or auto-sending campaigns that violate platform policies.
5. Do not provide financial guarantees, fake performance claims, or manipulated trading records.

## 2) Data Governance (Email and Contacts)

- Allowed:
  - Analyze mailbox metadata/content for the account owner's own business workflows.
  - Build contact lists only for authorized CRM use cases.
  - Process only data needed for defined tasks (data minimization).
- Required controls:
  - Keep a consent/provenance field for each contact.
  - Store purpose-of-use and retention period.
  - Support deletion and export on request.
  - Encrypt data at rest and in transit.
- Prohibited:
  - Selling or sharing contact data without explicit permission and legal basis.
  - Importing unknown third-party dumps into active campaigns.

## 3) Outreach and Monetization Controls

- Use opt-in lead generation (newsletter, gated content, waitlists, partnerships).
- Add clear unsubscribe and preference controls to every outreach channel.
- Respect anti-spam requirements (CAN-SPAM/GDPR/PECR and local equivalents).
- Keep domain reputation safeguards: warm-up, cadence caps, bounce monitoring.

## 4) Trading and Investment Controls

- Treat trading as high risk and non-guaranteed.
- Start with paper trading and validation windows before real capital.
- Enforce risk limits:
  - Max risk per trade (for example 0.5% to 1% of account).
  - Daily loss cap.
  - Stop trading after rule breach.
- Maintain a trade journal with setup, thesis, entry/exit, and post-trade review.
- Provide regulatory disclaimers in public content.

## 5) Financial Operations

- Record all inflows/outflows in an auditable ledger.
- Flag and review unusual transactions.
- Reconcile payment platform balances daily.
- Keep account destination details in secure config, not in prompts or source files.

## 6) Content and Course Production

- Clearly label education vs. financial advice.
- Use transparent claims backed by verifiable logs.
- Redact personal/sensitive data from screenshots, demos, and case studies.
- Track source licenses for media, templates, and datasets.

## 7) Enforcement Checklist (Run Before Any Automation)

1. Is this workflow using only authorized data sources?
2. Is there a lawful basis and consent trace for personal data?
3. Could this action be interpreted as spam, deception, or unauthorized access?
4. Are logs, retention, and deletion controls in place?
5. Does output include proper risk/compliance disclosures?

If any answer is "no", block execution and escalate to the Compliance Guardian.
