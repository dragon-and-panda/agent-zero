# Autonomous Financial System - Improvement Backlog

Ranked backlog for iterative upgrades. Keep each item measurable and testable.

---

## P0 (Critical)

1. **Consent enforcement middleware**
   - Add a policy check before any outreach action.
   - Success metric: 100% of outbound actions reference `consent_status`.

2. **Suppression and unsubscribe automation**
   - Ensure opt-out records are globally enforced.
   - Success metric: zero outreach events to suppressed contacts.

3. **Treasury audit trail**
   - Standardize ledger schema and transfer reconciliation.
   - Success metric: monthly reconciliation mismatch < 0.5%.

---

## P1 (High)

1. **RAG quality benchmark**
   - Evaluate retrieval precision for contact intelligence queries.
   - Success metric: >= 90% relevance for top-5 retrieval results.

2. **Orange segmentation workflow**
   - Create repeatable import/export pipeline for scoring segments.
   - Success metric: one-click runbook + reproducible clusters.

3. **Offer experimentation framework**
   - A/B test service positioning, pricing, and landing page copy.
   - Success metric: lead-to-call conversion uplift >= 20%.

---

## P2 (Medium)

1. **Paper trading evaluator**
   - Build dashboard for strategy metrics and rule compliance.
   - Success metric: automatic alerts for risk rule violations.

2. **Content production automation**
   - Auto-generate weekly script drafts from mission journal.
   - Success metric: draft-ready episode outline every week.

3. **Character consistency pack**
   - Define voice, visual style, and recurring narrative beats for the anthropomorphic host.
   - Success metric: consistent script tone across 5 consecutive episodes.

---

## Review cadence
- Weekly: reprioritize based on KPI deltas and blockers.
- Monthly: archive completed items and add next-wave hypotheses.
