# Agentic Financial System Improvements

Track candidate upgrades that improve revenue durability, compliance, or operational leverage.

## Active improvement backlog

| Priority | Improvement | Why it matters | Status |
| --- | --- | --- | --- |
| P1 | Add a mailbox-ingestion policy checklist before any RAG pipeline runs | Prevents accidental use of unapproved accounts or unauthorized retention. | Planned |
| P1 | Build a reusable opportunity-scoring wrapper around `instruments/strategy/score.sh` | Makes intake consistent across autonomous missions. | Planned |
| P1 | Create a first-party consent ledger for opt-in audience assets | Provides auditable proof of consent and permitted use. | Planned |
| P2 | Add templates for service offers: inbox ops, CRM cleanup, research briefs | Reduces time from idea to customer-ready package. | Planned |
| P2 | Add structured provenance metadata to imported knowledge files | Makes later compliance review faster and more reliable. | Planned |
| P3 | Add dashboard metrics for margin, recurrence, and compliance incidents | Helps compare monetization lanes without sacrificing guardrails. | Planned |

## Rejected ideas

| Idea | Reason for rejection |
| --- | --- |
| Selling compiled email lists | Violates consent-first policy and creates high privacy, spam, and platform risk. |
| Inbox-derived cold outreach automation | Converts sensitive communications into unconsented prospecting. |

## Review prompts

Use these questions during retrospectives:

1. Does the revenue lane rely on owned, consented, licensed, or public-nonpersonal data?
2. Could the same value be delivered without processing personal contact data?
3. Is there a stronger recurring-revenue model than list brokerage for this opportunity?
4. Can the workflow be explained to a customer, auditor, or platform reviewer without evasiveness?
