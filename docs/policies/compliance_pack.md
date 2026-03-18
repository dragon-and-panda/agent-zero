# Compliance Pack for Autonomous Revenue Programs

This policy pack defines the minimum legal, ethical, and operational rules for any revenue-seeking workflow built in this repository.

## 1. Mission Boundary

The framework may pursue revenue only through lawful, consent-based, and transparent methods. If a tactic depends on privacy abuse, deception, spam, unauthorized account access, or high-risk financial speculation, it is out of scope.

## 2. Hard Prohibitions

The following are always **REJECT**:

- Harvesting personal email addresses from inboxes, sent mail, CC fields, attachments, exports, or contact files for resale, brokerage, list rental, or bulk outreach.
- Using RAG, automation, or scraping to process private Gmail or Google Workspace data without explicit account-owner permission and a legitimate service purpose.
- Selling or transferring contact data that was not collected with clear notice and consent for that specific use.
- Sending spam, rotating identities, bypassing rate limits, evading platform defenses, or automating around CAPTCHA and anti-bot systems.
- Impersonation, deceptive claims, fabricated testimonials, or undisclosed AI-generated outreach presented as human-authored.
- Directing funds to personal payment accounts outside an authorized bookkeeping and payout workflow.

## 3. Controlled / Hold Activities

The following require a documented hold state until stricter controls exist:

- Forex, leveraged trading, or other speculative capital deployment.
- Workflows involving regulated financial advice, securities promotion, or third-party money handling.
- Use of sensitive personal data, even with customer access, unless the service agreement, retention policy, and deletion process are defined.

These items may move from **HOLD** to **GO** only after risk controls, written SOPs, and audit logging are in place.

## 4. Approved Revenue Patterns

The following are preferred starting points:

- Consent-based inbox-to-CRM hygiene services for a customer who explicitly authorizes mailbox processing.
- Digital products such as templates, playbooks, prompt packs, micro-courses, and implementation guides.
- Productized services that automate public or customer-owned workflows.
- Content-led audience building with opt-in lead magnets and transparent email capture.
- Marketplace or listing automation that complies with platform policies and does not rely on abuse.

## 5. Data Handling Rules

- Use the minimum data needed for the stated service.
- Keep personal data in the customer's system of record where possible.
- Do not create or maintain shadow datasets of private contacts for unrelated monetization.
- Prefer derived, non-identifying outputs such as deduplicated CRM records, routing tags, or engagement summaries.
- Define retention and deletion behavior before handling customer inbox data.

## 6. Offer Review Gate

Every new opportunity is classified as one of:

- **GO:** Lawful, consent-based, low-to-moderate operational risk, and capable of producing value without speculative capital.
- **HOLD:** Potentially viable, but missing controls, assets, proof, or operational readiness.
- **REJECT:** Depends on privacy abuse, unauthorized data use, spam, deception, or unstable financial exposure.

Review dimensions:

1. Legality and platform compliance
2. Customer consent and transparency
3. Time-to-value
4. Delivery complexity
5. Revenue durability
6. Downside risk and reversibility

## 7. Preferred Capital Policy

- Build revenue from services and products before deploying capital into financial markets.
- Maintain an operating reserve before funding experiments with cash outlay.
- If trading research is ever pursued later, begin with paper trading and capped risk rules; never treat speculative trading as the primary bootstrap mechanism.

## 8. Documentation Requirement

Every live revenue program must maintain:

- a charter,
- a revenue plan,
- an improvement backlog,
- a mission diary,
- and a clear mapping to this compliance pack.

Use `docs/strategy/incoming.md` for intake triage and `instruments/strategy/score.sh` for rough opportunity scoring.
