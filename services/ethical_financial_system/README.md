# Ethical Financial System Service (P0 Scaffold)

This service provides a consent-aware contact ingestion pipeline designed for legal outreach operations:

1. Ingest Gmail-style header data (received/sent/cc/bcc metadata).
2. Ingest CSV/CRM exports with explicit owner consent assertion.
3. Normalize and deduplicate addresses.
4. Persist contacts with compliance fields (`consent_status`, `suppression_flag`, source evidence).
5. Export Orange-ready CSV for segmentation and analysis.

It intentionally does **not** perform scraping or list-selling workflows.

## Quick Start

```bash
cd services/ethical_financial_system
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Overview

- `GET /health`
- `POST /contacts/ingest/headers`
- `POST /contacts/ingest/csv`
- `GET /contacts?owner_id=<id>`
- `GET /contacts/export/orange?owner_id=<id>`

## Sample: Header ingestion

```bash
curl -X POST http://localhost:8000/contacts/ingest/headers \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "owner_123",
    "owner_consent_asserted": true,
    "messages": [
      {
        "message_id": "msg-1",
        "from_addresses": ["Alice <alice@example.com>"],
        "to_addresses": ["bob@example.com"],
        "cc_addresses": ["carol@example.com"]
      }
    ]
  }'
```

## Sample: CSV ingestion

```bash
curl -X POST http://localhost:8000/contacts/ingest/csv \
  -H "Content-Type: application/json" \
  -d '{
    "owner_id": "owner_123",
    "owner_consent_asserted": true,
    "csv_content": "email,consent,suppressed\nalice@example.com,opted_in,0\nbob@example.com,opted_out,1\n",
    "email_column": "email",
    "consent_column": "consent",
    "suppression_column": "suppressed"
  }'
```

## Environment

- `EFS_DB_PATH` (default: `/workspace/tmp/ethical_financial_system.db`)

## Tests

```bash
cd services/ethical_financial_system
python -m unittest discover -s tests -p "test_*.py"
```
