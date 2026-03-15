from __future__ import annotations

import time
import uuid

from .. import schemas
from .ai_assistant import AIContractAssistant
from .escrow_adapter import EscrowAdapter
from .experience_memory import ExperienceMemory
from .store import HubStore
from .telemetry import TelemetryClient


class ContractOrchestrator:
    def __init__(
        self,
        store: HubStore,
        assistant: AIContractAssistant,
        escrow: EscrowAdapter,
        telemetry: TelemetryClient,
        memory: ExperienceMemory,
    ) -> None:
        self._store = store
        self._assistant = assistant
        self._escrow = escrow
        self._telemetry = telemetry
        self._memory = memory

    def create_thread(self, req: schemas.CreateThreadRequest) -> schemas.ContractThread:
        now = time.time()
        hints = self._memory.top_hints(req.intended_summary, limit=5)
        deliverables, ai_msg = self._assistant.draft_deliverables(
            intended_summary=req.intended_summary,
            context_notes=req.context_notes,
            learning_hints=hints,
        )
        thread = schemas.ContractThread(
            thread_id=str(uuid.uuid4()),
            created_at=now,
            updated_at=now,
            status=schemas.ThreadStatus.awaiting_ack,
            intended_summary=req.intended_summary,
            parties=[req.client, req.contractor],
            acknowledgements={req.client.id: False, req.contractor.id: False},
            messages=[ai_msg],
            deliverables=deliverables,
            terms=req.terms,
            learning_hints=hints,
        )
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "thread.created",
            thread.thread_id,
            {
                "deliverables": len(thread.deliverables),
                "parties": [p.id for p in thread.parties],
                "amount_usdt": thread.terms.amount_usdt,
            },
        )
        return thread

    def get_thread(self, thread_id: str) -> schemas.ContractThread:
        thread = self._store.get_thread(thread_id)
        if not thread:
            raise ValueError("Thread not found.")
        return thread

    def list_threads(self, limit: int = 100) -> list[schemas.ContractThread]:
        return self._store.list_threads(limit=limit)

    def add_message(self, thread_id: str, req: schemas.MessageCreate) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        if req.role not in (schemas.PartyRole.client, schemas.PartyRole.contractor):
            raise ValueError("Only client or contractor can send user messages.")
        if req.author_id not in thread.acknowledgements:
            raise ValueError("Unknown party for this thread.")

        message = schemas.ThreadMessage(
            message_id=str(uuid.uuid4()),
            role=req.role,
            author_id=req.author_id,
            content=req.content,
            created_at=time.time(),
        )
        thread.messages.append(message)
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "thread.message_added",
            thread.thread_id,
            {"role": req.role.value, "author_id": req.author_id},
        )
        return thread

    def refresh_scope(self, thread_id: str) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        transcript = " ".join(m.content for m in thread.messages[-12:])
        hints = self._memory.top_hints(f"{thread.intended_summary} {transcript}", limit=5)
        deliverables, ai_msg = self._assistant.draft_deliverables(
            intended_summary=thread.intended_summary,
            context_notes=transcript,
            learning_hints=hints,
        )
        thread.deliverables = deliverables
        thread.messages.append(ai_msg)
        thread.learning_hints = hints
        # Reset acknowledgements after scope change.
        thread.acknowledgements = {k: False for k in thread.acknowledgements.keys()}
        thread.status = schemas.ThreadStatus.awaiting_ack
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "thread.scope_refreshed",
            thread.thread_id,
            {"deliverables": len(thread.deliverables)},
        )
        return thread

    def acknowledge(self, thread_id: str, req: schemas.AcknowledgeRequest) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        if req.party_id not in thread.acknowledgements:
            raise ValueError("Party not part of this contract.")
        thread.acknowledgements[req.party_id] = True
        if all(thread.acknowledgements.values()):
            for d in thread.deliverables:
                d.status = schemas.DeliverableStatus.acknowledged
            thread.status = schemas.ThreadStatus.ready_for_funding
        else:
            thread.status = schemas.ThreadStatus.awaiting_ack
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "thread.acknowledged",
            thread.thread_id,
            {"party_id": req.party_id, "all_ack": all(thread.acknowledgements.values())},
        )
        return thread

    def fund_escrow(self, thread_id: str, req: schemas.FundEscrowRequest) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        if thread.status != schemas.ThreadStatus.ready_for_funding:
            raise ValueError("Both parties must acknowledge scope before funding.")
        self._escrow.fund(
            thread,
            amount_usdt=req.amount_usdt,
            tx_hash=req.tx_hash,
            contract_address=req.contract_address,
        )
        thread.status = schemas.ThreadStatus.funded
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "escrow.funded",
            thread.thread_id,
            {
                "amount_usdt": thread.escrow.amount_usdt,
                "tx_hash": thread.escrow.tx_hash,
            },
        )
        return thread

    def submit_evidence(
        self,
        thread_id: str,
        deliverable_id: str,
        req: schemas.EvidenceSubmissionRequest,
    ) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        deliverable = _find_deliverable(thread, deliverable_id)
        evidence = schemas.EvidenceItem(
            evidence_id=str(uuid.uuid4()),
            evidence_type=req.evidence_type,
            submitted_by=req.submitted_by,
            uri=req.uri,
            note=req.note,
            metadata=req.metadata,
            created_at=time.time(),
        )
        deliverable.evidence_submissions.append(evidence)
        deliverable.status = schemas.DeliverableStatus.submitted
        if thread.status in (
            schemas.ThreadStatus.funded,
            schemas.ThreadStatus.in_progress,
            schemas.ThreadStatus.remediation_required,
        ):
            thread.status = schemas.ThreadStatus.under_review
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "evidence.submitted",
            thread.thread_id,
            {
                "deliverable_id": deliverable_id,
                "evidence_type": req.evidence_type.value,
            },
        )
        return thread

    def run_ai_review(self, thread_id: str) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        if thread.escrow.status not in (
            schemas.EscrowStatus.funded,
            schemas.EscrowStatus.partially_released,
            schemas.EscrowStatus.locked_dispute,
        ):
            raise ValueError("Escrow must be funded before review.")

        result = self._assistant.review_deliverables(thread.deliverables)
        thread.latest_review = result
        if result.passed:
            thread.status = schemas.ThreadStatus.under_review
            for d in thread.deliverables:
                d.status = schemas.DeliverableStatus.accepted
            self._memory.add_lesson(
                "Successful completion correlated with explicit before/during/after evidence and objective acceptance criteria."
            )
        else:
            thread.status = schemas.ThreadStatus.remediation_required
            missing_map = {r.deliverable_id for r in result.remediation_actions}
            for d in thread.deliverables:
                d.status = (
                    schemas.DeliverableStatus.remediation_required
                    if d.deliverable_id in missing_map
                    else schemas.DeliverableStatus.accepted
                )

        thread.messages.append(
            schemas.ThreadMessage(
                message_id=str(uuid.uuid4()),
                role=schemas.PartyRole.ai,
                author_id="ai_contract_assistant",
                content=(
                    "Automated review complete. "
                    + ("All items passed." if result.passed else "Remediation addendum generated.")
                ),
                created_at=time.time(),
            )
        )
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "review.completed",
            thread.thread_id,
            {"passed": result.passed, "score": result.score},
        )
        return thread

    def release(self, thread_id: str, req: schemas.ReleaseRequest) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        self._escrow.release(
            thread=thread,
            to_contractor_usdt=req.to_contractor_usdt,
            to_platform_usdt=req.to_platform_usdt,
        )
        if thread.escrow.status == schemas.EscrowStatus.released:
            thread.status = schemas.ThreadStatus.completed
            self._memory.add_lesson(
                "On-time completion with complete evidence allows deterministic full release."
            )
        else:
            thread.status = schemas.ThreadStatus.in_progress
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "escrow.released",
            thread.thread_id,
            {
                "to_contractor_usdt": req.to_contractor_usdt,
                "to_platform_usdt": req.to_platform_usdt,
                "reason": req.reason,
                "remaining_usdt": self._escrow.remaining_balance(thread),
            },
        )
        return thread

    def raise_dispute(self, thread_id: str, req: schemas.RaiseDisputeRequest) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        self._escrow.lock_for_dispute(thread)
        thread.status = schemas.ThreadStatus.dispute
        thread.messages.append(
            schemas.ThreadMessage(
                message_id=str(uuid.uuid4()),
                role=schemas.PartyRole.system,
                author_id=req.raised_by,
                content=f"Dispute raised: {req.reason}",
                created_at=time.time(),
            )
        )
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "dispute.raised",
            thread.thread_id,
            {"raised_by": req.raised_by},
        )
        return thread

    def arbitrate(self, thread_id: str, req: schemas.ArbitrateRequest) -> schemas.ContractThread:
        thread = self.get_thread(thread_id)
        if thread.status != schemas.ThreadStatus.dispute:
            raise ValueError("Thread must be in dispute before arbitration.")

        remaining = self._escrow.remaining_balance(thread)
        requested = req.release_to_contractor_usdt + req.refund_to_client_usdt + req.platform_fee_usdt
        if abs(requested - remaining) > 1e-6:
            raise ValueError(
                "Arbitration split must allocate the full remaining escrow balance."
            )

        if req.release_to_contractor_usdt > 0 or req.platform_fee_usdt > 0:
            self._escrow.release(
                thread,
                to_contractor_usdt=req.release_to_contractor_usdt,
                to_platform_usdt=req.platform_fee_usdt,
            )
        if req.refund_to_client_usdt > 0:
            self._escrow.refund(thread, refund_to_client_usdt=req.refund_to_client_usdt)

        thread.arbitration = schemas.ArbitrationResolution(
            summary=req.summary,
            release_to_contractor_usdt=req.release_to_contractor_usdt,
            refund_to_client_usdt=req.refund_to_client_usdt,
            platform_fee_usdt=req.platform_fee_usdt,
            addendum=req.addendum,
            decided_at=time.time(),
        )
        thread.status = schemas.ThreadStatus.completed
        thread.messages.append(
            schemas.ThreadMessage(
                message_id=str(uuid.uuid4()),
                role=schemas.PartyRole.arbitrator,
                author_id="platform_arbitrator",
                content=f"Arbitration decision issued: {req.summary}",
                created_at=time.time(),
            )
        )
        self._memory.add_lesson(
            "Dispute resolution quality improves when remediation items explicitly map to each deliverable requirement."
        )
        self._touch(thread)
        self._store.upsert_thread(thread)
        self._telemetry.record_event(
            "dispute.resolved",
            thread.thread_id,
            {
                "contractor_usdt": req.release_to_contractor_usdt,
                "refund_usdt": req.refund_to_client_usdt,
                "platform_fee_usdt": req.platform_fee_usdt,
            },
        )
        return thread

    def _touch(self, thread: schemas.ContractThread) -> None:
        thread.updated_at = time.time()


def _find_deliverable(thread: schemas.ContractThread, deliverable_id: str) -> schemas.Deliverable:
    for d in thread.deliverables:
        if d.deliverable_id == deliverable_id:
            return d
    raise ValueError("Deliverable not found.")
