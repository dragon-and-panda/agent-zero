"""
Contractor Client Hub MCP Server.

Exposes contract workflow actions as MCP tools over stdio.
"""

from __future__ import annotations

from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from . import schemas
from .config import get_settings
from .services.ai_assistant import AIContractAssistant
from .services.escrow_adapter import EscrowAdapter
from .services.experience_memory import ExperienceMemory
from .services.mcp_router import MCPRouter
from .services.orchestrator import ContractOrchestrator
from .services.rag import RAGService
from .services.store import HubStore
from .services.telemetry import TelemetryClient

settings = get_settings()
mcp = FastMCP("contractor-client-hub")
orchestrator = ContractOrchestrator(
    store=HubStore(storage_path=settings.threads_path),
    assistant=AIContractAssistant(
        rag=RAGService(extra_corpus_paths=settings.rag_corpus_paths),
        mcp_router=MCPRouter(),
    ),
    escrow=EscrowAdapter(),
    telemetry=TelemetryClient(settings.telemetry_path),
    memory=ExperienceMemory(path=settings.experience_memory_path),
)


@mcp.tool()
def create_contract_thread(payload: Dict[str, Any]) -> Dict[str, Any]:
    req = schemas.CreateThreadRequest.model_validate(payload)
    return orchestrator.create_thread(req).model_dump(mode="json")


@mcp.tool()
def get_contract_thread(thread_id: str) -> Dict[str, Any]:
    return orchestrator.get_thread(thread_id).model_dump(mode="json")


@mcp.tool()
def list_contract_threads(limit: int = 100) -> List[Dict[str, Any]]:
    return [t.model_dump(mode="json") for t in orchestrator.list_threads(limit=limit)]


@mcp.tool()
def add_thread_message(thread_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    req = schemas.MessageCreate.model_validate(payload)
    return orchestrator.add_message(thread_id, req).model_dump(mode="json")


@mcp.tool()
def refresh_scope_with_ai(thread_id: str) -> Dict[str, Any]:
    return orchestrator.refresh_scope(thread_id).model_dump(mode="json")


@mcp.tool()
def acknowledge_scope(thread_id: str, party_id: str) -> Dict[str, Any]:
    req = schemas.AcknowledgeRequest(party_id=party_id)
    return orchestrator.acknowledge(thread_id, req).model_dump(mode="json")


@mcp.tool()
def fund_contract_escrow(
    thread_id: str,
    amount_usdt: float,
    tx_hash: str | None = None,
    contract_address: str | None = None,
) -> Dict[str, Any]:
    req = schemas.FundEscrowRequest(
        amount_usdt=amount_usdt,
        tx_hash=tx_hash,
        contract_address=contract_address,
    )
    return orchestrator.fund_escrow(thread_id, req).model_dump(mode="json")


@mcp.tool()
def submit_deliverable_evidence(
    thread_id: str,
    deliverable_id: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    req = schemas.EvidenceSubmissionRequest.model_validate(payload)
    return orchestrator.submit_evidence(thread_id, deliverable_id, req).model_dump(mode="json")


@mcp.tool()
def run_ai_evidence_review(thread_id: str) -> Dict[str, Any]:
    return orchestrator.run_ai_review(thread_id).model_dump(mode="json")


@mcp.tool()
def release_escrow(
    thread_id: str, to_contractor_usdt: float, to_platform_usdt: float, reason: str = "release"
) -> Dict[str, Any]:
    req = schemas.ReleaseRequest(
        to_contractor_usdt=to_contractor_usdt,
        to_platform_usdt=to_platform_usdt,
        reason=reason,
    )
    return orchestrator.release(thread_id, req).model_dump(mode="json")


@mcp.tool()
def raise_dispute(thread_id: str, raised_by: str, reason: str) -> Dict[str, Any]:
    req = schemas.RaiseDisputeRequest(raised_by=raised_by, reason=reason)
    return orchestrator.raise_dispute(thread_id, req).model_dump(mode="json")


@mcp.tool()
def arbitrate_dispute(thread_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    req = schemas.ArbitrateRequest.model_validate(payload)
    return orchestrator.arbitrate(thread_id, req).model_dump(mode="json")


@mcp.tool()
def contract_thread_schema() -> Dict[str, Any]:
    return schemas.ContractThread.model_json_schema()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
