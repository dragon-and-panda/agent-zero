# Commercial Compliance Policy Pack

This policy pack defines the minimum rules for revenue-generating workflows operated through Agent Zero.

---

## 1. Prohibited Activities

The system must not:

- harvest email addresses or personal contact details from inboxes, documents, websites, or third-party datasets for resale or unsolicited outreach,
- sell, rent, exchange, or otherwise monetize contact lists unless explicit permission exists for that exact use,
- scrape authenticated systems beyond the scope of authorized operations,
- perform deceptive outreach, impersonation, or undisclosed automation where disclosure is required,
- ignore unsubscribe, deletion, suppression, or retention obligations,
- repurpose customer or prospect data outside the scope in which it was collected.

---

## 2. Approved Uses of Communication Data

Authorized communication sources such as Gmail, helpdesk tools, or CRM notes may be used for:

- summarization,
- internal analytics,
- support operations,
- identifying product gaps,
- servicing existing customer relationships,
- routing and triage.

Before any extraction or storage, the workflow must verify:

1. source authorization,
2. business purpose,
3. minimum necessary fields,
4. outreach permission status,
5. retention rules.

---

## 3. Contact Handling Rules

Every contact record should carry:

- acquisition source,
- consent status,
- allowed communication channels,
- suppression / unsubscribe state,
- timestamp of last lawful basis review.

If any of these are unknown, the contact must be treated as **not outreach-eligible**.

---

## 4. Workflow Controls

Any tool or instrument that touches communications or contact data should:

- fail closed when consent metadata is missing,
- log source and purpose,
- avoid copying full message bodies unless required,
- redact restricted fields when passing context to non-essential components,
- support deletion and suppression propagation.

---

## 5. Escalation Triggers

Pause automation and require human review when:

- a workflow attempts to export contacts in bulk,
- the destination of personal data is unclear,
- the system cannot determine consent state,
- a platform terms-of-service conflict is detected,
- a jurisdiction-specific compliance question cannot be resolved from the policy pack.

---

## 6. Enforcement Guidance

The Compliance Governor described in `docs/autonomous_super_agency.md` should be treated as a blocking control, not an advisory role. If a monetization idea depends on harvested contacts, inbox mining for outreach, or list sales, the correct system response is to reject the workflow and propose an opt-in alternative.
