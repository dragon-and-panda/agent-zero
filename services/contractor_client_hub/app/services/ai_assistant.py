from __future__ import annotations

import re
import time
import uuid

from .. import schemas
from .mcp_router import MCPRouter
from .rag import RAGService


class AIContractAssistant:
    """Deterministic MVP assistant for contract drafting and evidence review."""

    def __init__(self, rag: RAGService, mcp_router: MCPRouter) -> None:
        self._rag = rag
        self._mcp_router = mcp_router

    def draft_deliverables(
        self,
        intended_summary: str,
        context_notes: str | None = None,
        learning_hints: list[str] | None = None,
    ) -> tuple[list[schemas.Deliverable], schemas.ThreadMessage]:
        material = " ".join(
            [intended_summary.strip(), (context_notes or "").strip(), *(learning_hints or [])]
        ).strip()
        line_items = _extract_line_items(material)
        rag_snippets = self._rag.retrieve(material, top_k=3)
        mcp_services = self._mcp_router.suggest_services(material)

        deliverables: list[schemas.Deliverable] = []
        for idx, item in enumerate(line_items, start=1):
            deliverables.append(
                schemas.Deliverable(
                    deliverable_id=str(uuid.uuid4()),
                    title=f"Deliverable {idx}",
                    scope_line_item=item,
                    contractor_expectations=[
                        f"Complete: {item}",
                        "Provide evidence package aligned to documentation plan.",
                        "Flag blockers within 24 hours of discovery.",
                    ],
                    client_expectations=[
                        "Provide timely access/approvals required for completion.",
                        "Review submitted evidence within agreed SLA.",
                        "Acknowledge acceptance or request remediation with specifics.",
                    ],
                    documentation_plan=_default_doc_plan(item),
                    evidence_requirements=_default_evidence_requirements(item),
                    status=schemas.DeliverableStatus.proposed,
                    ai_notes=[f"RAG context: {rag_snippets[0]}" if rag_snippets else "RAG context unavailable."],
                )
            )

        ai_message = schemas.ThreadMessage(
            message_id=str(uuid.uuid4()),
            role=schemas.PartyRole.ai,
            author_id="ai_contract_assistant",
            content=(
                "Generated contract line items, expectations, and documentation/evidence requirements. "
                "Please review and edit any deliverable before acknowledgements."
            ),
            created_at=time.time(),
            rag_sources=rag_snippets,
            mcp_services_used=mcp_services,
        )
        return deliverables, ai_message

    def review_deliverables(self, deliverables: list[schemas.Deliverable]) -> schemas.ReviewResult:
        notes: list[str] = []
        remediations: list[schemas.RemediationAction] = []
        fulfilled = 0

        for d in deliverables:
            missing = _missing_evidence(d)
            if missing:
                remediations.append(
                    schemas.RemediationAction(
                        deliverable_id=d.deliverable_id,
                        summary=f"Deliverable '{d.title}' requires additional evidence.",
                        required_fixes=missing,
                        suggested_partial_release_usdt=0.0,
                    )
                )
                notes.append(f"{d.title}: evidence incomplete.")
            else:
                fulfilled += 1
                notes.append(f"{d.title}: evidence complete.")

        total = len(deliverables) or 1
        score = round((fulfilled / total) * 100.0, 2)
        passed = fulfilled == len(deliverables) and len(deliverables) > 0
        if passed:
            notes.insert(0, "All deliverables passed automated evidence checks.")
        else:
            notes.insert(0, "Automated review found missing or weak completion evidence.")

        return schemas.ReviewResult(
            passed=passed,
            score=score,
            notes=notes,
            remediation_actions=remediations,
        )


def _extract_line_items(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ["Complete the agreed scope with documented evidence and acceptance."]
    parts = re.split(r"[.;\n]|(?:\band\b)", text)
    cleaned = []
    for part in parts:
        p = part.strip(" ,-")
        if len(p) < 20:
            continue
        cleaned.append(p[0].upper() + p[1:] if p else p)
    if not cleaned:
        return [text]
    # Keep concise scope to avoid over-fragmented contracts.
    return cleaned[:8]


def _default_doc_plan(item: str) -> list[schemas.DocumentationInstruction]:
    return [
        schemas.DocumentationInstruction(
            phase="before",
            instruction=f"Capture baseline condition and pre-work checklist for: {item}.",
        ),
        schemas.DocumentationInstruction(
            phase="during",
            instruction="Capture midpoint evidence (photos/videos/notes) at key checkpoints.",
        ),
        schemas.DocumentationInstruction(
            phase="after",
            instruction="Capture completion evidence and summarize adherence to agreed standards.",
        ),
    ]


def _default_evidence_requirements(item: str) -> list[schemas.EvidenceRequirement]:
    requirements: list[schemas.EvidenceRequirement] = [
        schemas.EvidenceRequirement(
            evidence_type=schemas.EvidenceType.photo,
            requirement=f"At least 2 photos proving completion for: {item}.",
            minimum_count=2,
        ),
        schemas.EvidenceRequirement(
            evidence_type=schemas.EvidenceType.document,
            requirement="Completion report or checklist signed/acknowledged by responsible party.",
            minimum_count=1,
        ),
    ]
    lowered = item.lower()
    if any(k in lowered for k in ("code", "standard", "permit", "inspection", "authority")):
        requirements.append(
            schemas.EvidenceRequirement(
                evidence_type=schemas.EvidenceType.permit,
                requirement="Attach permit/code compliance record where applicable.",
                minimum_count=1,
                authority_reference="local_authority_or_standard_reference",
            )
        )
    return requirements


def _missing_evidence(deliverable: schemas.Deliverable) -> list[str]:
    missing: list[str] = []
    by_type: dict[schemas.EvidenceType, int] = {}
    for item in deliverable.evidence_submissions:
        by_type[item.evidence_type] = by_type.get(item.evidence_type, 0) + 1
    for req in deliverable.evidence_requirements:
        have = by_type.get(req.evidence_type, 0)
        if have < req.minimum_count:
            missing.append(
                f"{req.evidence_type.value}: requires {req.minimum_count}, found {have}. {req.requirement}"
            )
    return missing
