import csv
import io

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

from .config import get_settings
from .schemas import (
    ConsentStatus,
    ContactRecord,
    CsvIngestionRequest,
    HeaderIngestionRequest,
    IngestionResponse,
)
from .services.ingestion import ContactIngestionService
from .services.store import ContactStore

app = FastAPI(
    title="Ethical Financial System Service",
    description="Consent-aware contact ingestion and compliance-friendly contact operations.",
    version="0.1.0",
)

store = ContactStore(get_settings().db_path)
ingestion = ContactIngestionService(store=store)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


def _to_contact_record(row) -> ContactRecord:
    return ContactRecord(
        owner_id=row.owner_id,
        email=row.email,
        consent_status=ConsentStatus(row.consent_status),
        suppression_flag=bool(row.suppression_flag),
        sources=row.sources,
        first_seen_at=row.first_seen_at,
        last_seen_at=row.last_seen_at,
        evidence_count=row.evidence_count,
        last_source=row.last_source,
    )


@app.post("/contacts/ingest/headers", response_model=IngestionResponse)
async def ingest_headers(payload: HeaderIngestionRequest) -> IngestionResponse:
    try:
        summary, emails = ingestion.ingest_headers(payload)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    contacts = store.get_contacts_by_emails(payload.owner_id, emails)
    return IngestionResponse(summary=summary, touched_contacts=[_to_contact_record(c) for c in contacts])


@app.post("/contacts/ingest/csv", response_model=IngestionResponse)
async def ingest_csv(payload: CsvIngestionRequest) -> IngestionResponse:
    try:
        summary, emails = ingestion.ingest_csv(payload)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    contacts = store.get_contacts_by_emails(payload.owner_id, emails)
    return IngestionResponse(summary=summary, touched_contacts=[_to_contact_record(c) for c in contacts])


@app.get("/contacts", response_model=list[ContactRecord])
async def list_contacts(
    owner_id: str,
    consent_status: ConsentStatus | None = None,
    suppression_flag: bool | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
) -> list[ContactRecord]:
    rows = store.list_contacts(
        owner_id=owner_id,
        consent_status=consent_status.value if consent_status else None,
        suppression_flag=suppression_flag,
        limit=limit,
    )
    return [_to_contact_record(row) for row in rows]


@app.get("/contacts/export/orange", response_class=PlainTextResponse)
async def export_orange_csv(owner_id: str, limit: int = Query(default=1000, ge=1, le=50000)) -> str:
    rows = store.list_contacts(owner_id=owner_id, limit=limit)

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(
        [
            "email",
            "consent_status",
            "suppression_flag",
            "source_count",
            "sources",
            "evidence_count",
            "first_seen_at",
            "last_seen_at",
        ]
    )
    for row in rows:
        writer.writerow(
            [
                row.email,
                row.consent_status,
                int(row.suppression_flag),
                len(row.sources),
                "|".join(sorted(row.sources)),
                row.evidence_count,
                row.first_seen_at,
                row.last_seen_at,
            ]
        )

    return out.getvalue()
