from __future__ import annotations

from fastapi import FastAPI, HTTPException

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

app = FastAPI(
    title="Contractor Client Hub",
    description=(
        "AI-assisted contract drafting and escrow workflow with evidence review, "
        "remediation addendum, and arbitration state transitions."
    ),
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/threads", response_model=schemas.ContractThread)
async def create_thread(req: schemas.CreateThreadRequest) -> schemas.ContractThread:
    try:
        return orchestrator.create_thread(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/threads/{thread_id}", response_model=schemas.ContractThread)
async def get_thread(thread_id: str) -> schemas.ContractThread:
    try:
        return orchestrator.get_thread(thread_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/threads", response_model=list[schemas.ContractThread])
async def list_threads(limit: int = 100) -> list[schemas.ContractThread]:
    return orchestrator.list_threads(limit=limit)


@app.post("/threads/{thread_id}/messages", response_model=schemas.ContractThread)
async def add_message(
    thread_id: str, req: schemas.MessageCreate
) -> schemas.ContractThread:
    try:
        return orchestrator.add_message(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/ai/refresh-scope", response_model=schemas.ContractThread)
async def refresh_scope(thread_id: str) -> schemas.ContractThread:
    try:
        return orchestrator.refresh_scope(thread_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/acknowledge", response_model=schemas.ContractThread)
async def acknowledge(
    thread_id: str, req: schemas.AcknowledgeRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.acknowledge(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/escrow/fund", response_model=schemas.ContractThread)
async def fund_escrow(
    thread_id: str, req: schemas.FundEscrowRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.fund_escrow(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/threads/{thread_id}/deliverables/{deliverable_id}/evidence",
    response_model=schemas.ContractThread,
)
async def submit_evidence(
    thread_id: str,
    deliverable_id: str,
    req: schemas.EvidenceSubmissionRequest,
) -> schemas.ContractThread:
    try:
        return orchestrator.submit_evidence(thread_id, deliverable_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/ai/review", response_model=schemas.ContractThread)
async def run_ai_review(thread_id: str) -> schemas.ContractThread:
    try:
        return orchestrator.run_ai_review(thread_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/escrow/release", response_model=schemas.ContractThread)
async def release_escrow(
    thread_id: str, req: schemas.ReleaseRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.release(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/dispute", response_model=schemas.ContractThread)
async def raise_dispute(
    thread_id: str, req: schemas.RaiseDisputeRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.raise_dispute(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/arbitrate", response_model=schemas.ContractThread)
async def arbitrate(
    thread_id: str, req: schemas.ArbitrateRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.arbitrate(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
