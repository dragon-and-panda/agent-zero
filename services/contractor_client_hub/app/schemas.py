from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PartyRole(str, Enum):
    client = "client"
    contractor = "contractor"
    ai = "ai"
    system = "system"
    arbitrator = "arbitrator"


class ThreadStatus(str, Enum):
    drafting = "drafting"
    awaiting_ack = "awaiting_ack"
    ready_for_funding = "ready_for_funding"
    funded = "funded"
    in_progress = "in_progress"
    under_review = "under_review"
    remediation_required = "remediation_required"
    dispute = "dispute"
    completed = "completed"
    closed = "closed"


class DeliverableStatus(str, Enum):
    proposed = "proposed"
    acknowledged = "acknowledged"
    in_progress = "in_progress"
    submitted = "submitted"
    accepted = "accepted"
    remediation_required = "remediation_required"


class EvidenceType(str, Enum):
    photo = "photo"
    document = "document"
    video = "video"
    checklist = "checklist"
    signature = "signature"
    permit = "permit"
    code_report = "code_report"
    other = "other"


class EscrowStatus(str, Enum):
    none = "none"
    funded = "funded"
    partially_released = "partially_released"
    released = "released"
    locked_dispute = "locked_dispute"
    refunded = "refunded"


class Party(BaseModel):
    id: str = Field(..., description="Unique participant id from your identity provider.")
    role: PartyRole
    display_name: str
    wallet_address: str | None = Field(
        default=None, description="Optional wallet address for escrow disbursement."
    )


class ThreadMessage(BaseModel):
    message_id: str
    role: PartyRole
    author_id: str
    content: str
    created_at: float
    rag_sources: list[str] = Field(default_factory=list)
    mcp_services_used: list[str] = Field(default_factory=list)


class MessageCreate(BaseModel):
    role: PartyRole = Field(
        ..., description="Must be client or contractor for user-authored messages."
    )
    author_id: str
    content: str = Field(..., min_length=1)


class DocumentationInstruction(BaseModel):
    phase: str = Field(
        ..., description="Expected values: before, during, after, or handoff."
    )
    instruction: str


class EvidenceRequirement(BaseModel):
    evidence_type: EvidenceType
    requirement: str
    minimum_count: int = Field(default=1, ge=1, le=50)
    authority_reference: str | None = Field(
        default=None, description="Optional local code or quality standard reference."
    )


class EvidenceItem(BaseModel):
    evidence_id: str
    evidence_type: EvidenceType
    submitted_by: str
    uri: str
    note: str | None = None
    created_at: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvidenceSubmissionRequest(BaseModel):
    submitted_by: str
    evidence_type: EvidenceType
    uri: str
    note: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Deliverable(BaseModel):
    deliverable_id: str
    title: str
    scope_line_item: str = Field(
        ..., description="Human-readable expectation both parties acknowledge."
    )
    contractor_expectations: list[str] = Field(default_factory=list)
    client_expectations: list[str] = Field(default_factory=list)
    documentation_plan: list[DocumentationInstruction] = Field(default_factory=list)
    evidence_requirements: list[EvidenceRequirement] = Field(default_factory=list)
    evidence_submissions: list[EvidenceItem] = Field(default_factory=list)
    status: DeliverableStatus = DeliverableStatus.proposed
    ai_notes: list[str] = Field(default_factory=list)


class ContractTerms(BaseModel):
    network: str = "polygon"
    token: str = "USDT"
    amount_usdt: float = Field(..., gt=0)
    platform_fee_percent: float = Field(
        ..., ge=5, le=30, description="Platform fee for mediation/automation services."
    )
    arbitration_required: bool = True
    arbitration_policy: str = (
        "Both parties agree to binding platform arbitration for unresolved completion disputes."
    )


class EscrowRecord(BaseModel):
    status: EscrowStatus = EscrowStatus.none
    amount_usdt: float = 0.0
    network: str = "polygon"
    token: str = "USDT"
    contract_address: str | None = None
    tx_hash: str | None = None
    funded_at: float | None = None
    released_to_contractor_usdt: float = 0.0
    released_to_platform_usdt: float = 0.0
    refunded_to_client_usdt: float = 0.0


class RemediationAction(BaseModel):
    deliverable_id: str
    summary: str
    required_fixes: list[str] = Field(default_factory=list)
    suggested_partial_release_usdt: float = Field(default=0.0, ge=0)


class ReviewResult(BaseModel):
    passed: bool
    score: float = Field(..., ge=0, le=100)
    notes: list[str] = Field(default_factory=list)
    remediation_actions: list[RemediationAction] = Field(default_factory=list)


class ArbitrationResolution(BaseModel):
    decided_by: str = "platform_arbitrator"
    summary: str
    release_to_contractor_usdt: float = Field(default=0.0, ge=0)
    refund_to_client_usdt: float = Field(default=0.0, ge=0)
    platform_fee_usdt: float = Field(default=0.0, ge=0)
    addendum: list[str] = Field(default_factory=list)
    decided_at: float


class ContractThread(BaseModel):
    thread_id: str
    created_at: float
    updated_at: float
    status: ThreadStatus = ThreadStatus.drafting
    intended_summary: str
    parties: list[Party] = Field(default_factory=list)
    acknowledgements: dict[str, bool] = Field(default_factory=dict)
    messages: list[ThreadMessage] = Field(default_factory=list)
    deliverables: list[Deliverable] = Field(default_factory=list)
    terms: ContractTerms
    escrow: EscrowRecord = Field(default_factory=EscrowRecord)
    latest_review: ReviewResult | None = None
    arbitration: ArbitrationResolution | None = None
    learning_hints: list[str] = Field(default_factory=list)


class CreateThreadRequest(BaseModel):
    intended_summary: str = Field(..., min_length=20)
    client: Party
    contractor: Party
    terms: ContractTerms
    context_notes: str | None = Field(
        default=None,
        description="Optional details to improve initial scope breakdown and evidence plan.",
    )


class AcknowledgeRequest(BaseModel):
    party_id: str


class FundEscrowRequest(BaseModel):
    amount_usdt: float = Field(..., gt=0)
    tx_hash: str | None = None
    contract_address: str | None = None


class ReleaseRequest(BaseModel):
    to_contractor_usdt: float = Field(..., ge=0)
    to_platform_usdt: float = Field(..., ge=0)
    reason: str = "release"


class RaiseDisputeRequest(BaseModel):
    raised_by: str
    reason: str = Field(..., min_length=10)


class ArbitrateRequest(BaseModel):
    summary: str = Field(..., min_length=10)
    release_to_contractor_usdt: float = Field(..., ge=0)
    refund_to_client_usdt: float = Field(..., ge=0)
    platform_fee_usdt: float = Field(default=0.0, ge=0)
    addendum: list[str] = Field(default_factory=list)
