# Compliance Pack for Autonomous Revenue Workflows

This policy pack defines the minimum legal, privacy, and ethics rules for any Agent Zero workflow that touches customer data, outreach, monetization, or market operations.

## 1. Purpose

Autonomous agents must pursue revenue using lawful, consent-based, and non-deceptive methods. The framework may automate research, product development, analytics, and operations, but it must not be used to harvest personal data, enable spam, or trade in contact information.

## 2. Hard Prohibitions

The following actions are disallowed:

- Accessing, mining, or summarizing personal email inboxes, direct messages, or cloud accounts for monetization without a clear, documented business purpose and the account owner's explicit authorization.
- Extracting, compiling, enriching, selling, renting, sharing, or brokering personal email addresses or contact lists.
- Scraping hidden, gated, or private personal data from websites, SaaS platforms, or uploaded files.
- Generating or sending spam, mass unsolicited outreach, or deceptive lead-generation campaigns.
- Circumventing authentication, rate limits, consent flows, or platform restrictions.
- Misrepresenting identity, affiliation, or intent during research, outreach, or sales.
- Processing regulated or sensitive personal data unless the workflow has a documented lawful basis, storage controls, and a specific compliance review.

## 3. Allowed Data Sources

Agents may use:

- First-party analytics, product telemetry, and transaction data collected by the operator.
- User-uploaded files that the operator has the right to analyze for the stated purpose.
- Internal knowledge bases, SOPs, and documents stored in `knowledge/`, `docs/`, and `memory/`.
- Public, non-private business information used for market research, pricing analysis, or competitive intelligence.
- Opt-in CRM or newsletter data when consent status and intended use are recorded.

## 4. Consent and Outreach Rules

Before any outreach or contact management workflow is enabled:

1. Consent source must be recorded.
2. Intended message category must be defined (transactional, support, newsletter, sales, etc.).
3. Unsubscribe and suppression handling must exist.
4. Jurisdictional rules must be checked for the recipient region.
5. Outreach volume must remain proportional and reviewable.

Double opt-in is preferred for newsletters, waitlists, and promotions.

## 5. Revenue Patterns That Are In Bounds

Examples of acceptable monetization:

- Selling software, templates, reports, or automation services.
- Running affiliate content with clear disclosures.
- Building opt-in newsletters or communities and monetizing through sponsorships.
- Offering research, implementation, or operational services to businesses.
- Using RAG over owned or licensed documents to improve internal productivity or customer support.

## 6. Revenue Patterns That Are Out of Bounds

Examples of unacceptable monetization:

- Selling email lists, lead dumps, or scraped contact databases.
- Turning private inbox data into prospecting assets.
- Scraping personal contacts from resumes, spreadsheets, or account exports for resale.
- Sending cold bulk outreach sourced from harvested personal data.

## 7. Jurisdictional Baseline

This framework should be configured with the assumption that the operator may need to satisfy:

- GDPR and ePrivacy rules for EU/EEA data subjects
- CCPA/CPRA-style privacy rights for California residents
- CAN-SPAM and similar anti-spam rules for email marketing
- Platform-specific developer and acceptable-use policies

This file is not legal advice. It is an operational minimum, not a substitute for counsel.

## 8. Agent Decision Checklist

Before running a monetization or data pipeline, the responsible agent should be able to answer yes to all of the following:

- Do we have the right to access this data?
- Is the use aligned with the data subject's expectations and consent?
- Are we avoiding personal-data resale and spam?
- Is the workflow transparent, reviewable, and reversible?
- Would a reasonable user consider this use ethical and non-deceptive?

If any answer is no or unclear, stop the workflow and escalate for review.
