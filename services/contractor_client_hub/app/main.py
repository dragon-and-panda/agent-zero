from __future__ import annotations

import hashlib
import hmac
import json

from fastapi import FastAPI, HTTPException, Header, Request

from . import schemas
from .config import get_settings
from .services.ai_assistant import AIContractAssistant
from .services.email_gateway import EmailGateway
from .services.escrow_adapter import EscrowAdapter
from .services.experience_memory import ExperienceMemory
from .services.mcp_router import MCPRouter
from .services.meeting_provider import MeetingProvider
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
    meeting_provider=MeetingProvider(
        room_base_url=settings.realtime_room_base_url,
        signing_secret=settings.realtime_token_secret,
        ttl_seconds=settings.realtime_token_ttl_seconds,
    ),
    email_gateway=EmailGateway(
        provider=settings.email_provider,
        from_address=settings.email_from_address,
        relay_endpoint=settings.email_relay_endpoint,
        relay_bearer_token=settings.email_relay_bearer_token,
        outbox_path=settings.email_outbox_path,
    ),
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


@app.post("/threads/{thread_id}/bids", response_model=schemas.ContractThread)
async def submit_bid(
    thread_id: str, req: schemas.ContractorBidRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.submit_bid(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/meetings", response_model=schemas.ContractThread)
async def create_meeting(
    thread_id: str, req: schemas.CreateMeetingRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.create_meeting(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/threads/{thread_id}/meetings/{meeting_id}/events",
    response_model=schemas.ContractThread,
)
async def add_meeting_event(
    thread_id: str, meeting_id: str, req: schemas.MeetingEventRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.add_meeting_event(thread_id, meeting_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/threads/{thread_id}/meetings/{meeting_id}/join-token",
    response_model=schemas.MeetingJoinTokenResponse,
)
async def issue_join_token(
    thread_id: str, meeting_id: str, req: schemas.MeetingJoinTokenRequest
) -> schemas.MeetingJoinTokenResponse:
    try:
        return orchestrator.issue_meeting_join_token(thread_id, meeting_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/threads/{thread_id}/meetings/{meeting_id}/end",
    response_model=schemas.ContractThread,
)
async def end_meeting(
    thread_id: str, meeting_id: str, req: schemas.EndMeetingRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.end_meeting(thread_id, meeting_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/ai/refresh-scope", response_model=schemas.ContractThread)
async def refresh_scope(thread_id: str) -> schemas.ContractThread:
    try:
        return orchestrator.refresh_scope(thread_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/progress-reports", response_model=schemas.ContractThread)
async def create_progress_report(
    thread_id: str, req: schemas.ProgressReportRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.create_progress_report(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/emails/draft", response_model=schemas.ContractThread)
async def draft_progress_email(
    thread_id: str, req: schemas.ProgressEmailRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.draft_progress_email(thread_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/threads/{thread_id}/emails/{email_id}/sent",
    response_model=schemas.ContractThread,
)
async def mark_email_sent(
    thread_id: str, email_id: str, req: schemas.MarkEmailSentRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.mark_email_sent(thread_id, email_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/threads/{thread_id}/emails/{email_id}/send", response_model=schemas.ContractThread)
async def send_email(
    thread_id: str, email_id: str, req: schemas.SendEmailRequest
) -> schemas.ContractThread:
    try:
        return orchestrator.send_progress_email(thread_id, email_id, req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/integrations/email/webhook")
async def handle_email_webhook(
    request: Request,
    x_cch_signature: str | None = Header(default=None),
) -> dict:
    raw_body = await request.body()
    if settings.email_webhook_secret:
        if not _valid_signature(
            raw=raw_body,
            signature_header=x_cch_signature,
            secret=settings.email_webhook_secret,
        ):
            raise HTTPException(status_code=401, detail="Invalid webhook signature.")
    try:
        payload = json.loads(raw_body.decode("utf-8"))
        event = schemas.EmailWebhookEventRequest.model_validate(payload)
        orchestrator.apply_email_webhook(event)
        return {"status": "ok", "email_id": event.email_id, "thread_id": event.thread_id}
    except (json.JSONDecodeError, ValueError) as exc:
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


def _valid_signature(raw: bytes, signature_header: str | None, secret: str) -> bool:
    if not signature_header:
        return False
    provided = signature_header.strip()
    if provided.startswith("sha256="):
        provided = provided.split("=", 1)[1]
    digest = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(provided, digest)
