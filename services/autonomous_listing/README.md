# Autonomous Listing Service (MVP Scaffold)

This folder contains a FastAPI-based microservice that simulates the AI pipeline defined in `docs/autonomous_listing_service.md`. It is not production-ready yet, but it provides a runnable skeleton that:

1. Accepts listing requests with seller notes, assets, preferences, and target platforms.
2. Runs through pluggable pipelines for image enhancement (vision API stub), marketing copy (OpenAI + RAG hook), and multi-platform publishing.
3. Returns a structured preview containing the listing status, suggested price, generated description, enhanced asset URIs, and per-platform states.

## Quick Start

```bash
cd services/autonomous_listing
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run as an MCP Server (stdio)

This exposes the existing orchestrator pipeline as MCP tools (intended for Claude Desktop / Cursor / any MCP client).

```bash
cd services/autonomous_listing
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.mcp_server
```

Available tools include:
- `create_listing(payload)` → returns `ListingResponse`
- `create_listing_draft(payload)` → generates best-in-class copy/variants without publishing
- `validate_listing_request(payload)` → returns normalized payload
- `list_supported_platforms()` → returns platform ids

POST a sample request:

```bash
curl -X POST http://localhost:8000/listings \
  -H "Content-Type: application/json" \
  -d '{
    "raw_description": "Mid-century walnut coffee table, gentle wear, includes glass top.",
    "category": "furniture",
    "location": "Austin, TX",
    "assets": [{"source_uri": "https://example.com/photo1.jpg"}],
    "target_platforms": ["craigslist", "mercari"],
    "preferences": {"tone": "premium", "target_price": 350}
  }'
```

## Next Steps
- Provide production credentials:
  - `ALS_OPENAI_API_KEY` / `ALS_OPENAI_MODEL`
  - `ALS_MARKETING_RAG_ENDPOINT`
  - `ALS_VISION_API_BASE` / `ALS_VISION_API_KEY`
  - `ALS_CRAIGSLIST_EMAIL`, `ALS_MERCARI_API_KEY`
- Replace placeholder adapters (Craigslist Playwright flow, Mercari API stub) with full automation and add more marketplaces.
- Connect to object storage for asset handling and to the knowledge/memory layers described in the main blueprint.
- Built-in telemetry writes JSON lines to `/workspace/logs/listings/events.log` (override with `LISTING_TELEMETRY_PATH`). Extend or pipe these events into your observability stack.
- Embed mission-diary hooks so the service feeds the agency’s iterative improvement loop.
