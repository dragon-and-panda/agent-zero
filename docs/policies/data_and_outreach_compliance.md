# Data and Outreach Compliance Policy

This policy applies to all data extraction, enrichment, retrieval, and messaging workflows in this repository.

---

## 1. Purpose

Ensure all growth and revenue activities are legal, ethical, and auditable.

---

## 2. Hard Prohibitions

- No selling personal email lists.
- No purchasing stolen or unverified contact datasets.
- No mailbox scraping without authenticated owner permission.
- No outreach to contacts with unknown or denied consent state.
- No attempts to bypass platform security, anti-spam, or anti-abuse controls.

---

## 3. Allowed Contact States

- `opt_in`: explicit permission for marketing outreach.
- `transactional_only`: service/relationship communication only.
- `do_not_contact`: never send outreach.
- `unknown`: treat as `do_not_contact` until consent is obtained.

---

## 4. Minimum Logging Requirements

For each contact record and campaign send:
- source system and ingestion timestamp,
- consent source/evidence,
- processing steps and transformations,
- suppression checks result,
- sender identity and campaign ID.

---

## 5. Enforcement Rules

- Campaign execution must fail closed if consent metadata is missing.
- Suppression lists are mandatory and cannot be bypassed.
- Compliance governor has authority to pause all outbound workflows on violation.

---

## 6. Incident Response

1. Stop affected workflow immediately.
2. Identify impacted records and channels.
3. Notify stakeholders and log corrective action.
4. Patch process and run regression checks before restart.

