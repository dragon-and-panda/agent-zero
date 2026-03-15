# Contractor Client Hub — Program Blueprint

This program defines an AI-assisted, evidence-driven contractor/client workflow with escrow and dispute resolution support.

---

## 1. Mission

Create a fair and auditable platform where clients and contractors can:
- co-author scope in a chat thread with AI support,
- lock milestones and expectations,
- submit and verify completion evidence,
- resolve payment via escrow disbursement,
- handle disputes through remediation and arbitration.

---

## 2. Product Pillars

1. **AI Contract Composer**
   - Starts with intended deliverable summary.
   - Breaks work into line-item deliverables with plain-language expectations for both parties.
2. **Evidence Protocol**
   - Every deliverable includes `before`, `during`, and `after` documentation instructions.
   - Requires objective proof artifacts (photos, docs, permits/codes where relevant).
3. **Escrow Safety**
   - Client stakes token amount (USDT MVP) into escrow.
   - Release is based on accepted completion evidence or arbitration resolution.
4. **Fair Resolution**
   - AI proposes remediation addendum for discrepancies.
   - Platform arbitration handles unresolved conflicts with predefined binding policy.
5. **Learning Loop**
   - System stores lessons learned from each thread to improve future scope quality and review heuristics.

---

## 3. Workflow State Machine

1. `drafting`
2. `awaiting_ack`
3. `ready_for_funding`
4. `funded`
5. `under_review` / `remediation_required`
6. `dispute` (if raised)
7. `completed`

---

## 4. Core Artifacts

- Contract thread transcript
- AI-generated deliverables
- Documentation plan per deliverable
- Evidence submission log
- Review results + remediation addendum
- Escrow ledger transitions
- Arbitration resolution record

---

## 5. Commercial Model

Platform fee ranges from **5% to 30%** depending on involvement:
- Low-touch automation (near 5%)
- Active remediation/arbitration or complex oversight (higher band)

---

## 6. Compliance & Safety

- Transparent terms and acknowledgment from both parties.
- Explicit evidence criteria before work starts.
- Human override and arbitration controls for edge cases.
- Smart-contract deployment requires professional audit before production usage.

---

## 7. Build Targets

### MVP
- FastAPI backend with chat + contract state machine
- Escrow adapter abstraction
- AI drafting/review heuristics with RAG context
- MCP server for agent interoperability
- Solidity reference contract + desktop validation UI

### Next
- Production wallet orchestration and on-chain event indexing
- Frontend dashboard for both parties
- Computer vision and document-verification models for stronger evidence scoring
