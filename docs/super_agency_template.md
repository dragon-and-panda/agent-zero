## Super Agency Template (Repo Pattern)

This repository can be used as a **“super agency” template**: a core multi-agent runtime plus a set of optional **capability services** that can be exposed as APIs and/or **MCP servers**.

### Core layers

- **Agent runtime**: `agent.py`, `python/`, `prompts/`, `memory/`, `knowledge/`, `instruments/`
- **Capability services**: `services/*` (each service owns its own deps, config, and API surface)
- **MCP adapters**: small wrappers that expose a capability as MCP tools/resources (stdio by default)

### How to customize this template

- **Behavior + skills**
  - Fork or copy `prompts/default/` into `prompts/<your_org>/` and edit.
  - Add instruments in `instruments/custom/` for low-token reusable procedures.
- **Knowledge**
  - Put org-specific docs into `knowledge/custom/` and keep them versioned.
- **Services**
  - Add new capabilities under `services/<capability_name>/` with:
    - `app/` (business logic)
    - `app/main.py` (FastAPI or other API)
    - `app/mcp_server.py` (MCP stdio server wrapper, optional)
    - `requirements.txt` (service-local dependency lock)
- **Configuration**
  - Extend `example.env` with your service-specific env vars (prefer a dedicated prefix per service).

### Autonomous Listing MCP server (implemented)

The existing listing pipeline in `services/autonomous_listing` is exposed as an MCP stdio server at:

- `services/autonomous_listing/app/mcp_server.py`

Tools:

- `create_listing(payload)` → returns a `ListingResponse` JSON object
- `validate_listing_request(payload)` → returns validated payload with defaults applied
- `list_supported_platforms()` → returns supported platform ids
- `listing_request_schema()` / `listing_response_schema()` → JSON schema helpers

Run it:

```bash
cd services/autonomous_listing
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.mcp_server
```

### Revenue Planner MCP server (implemented)

The compliant revenue-planning workflow in `services/revenue_planner` is exposed as an MCP stdio server at:

- `services/revenue_planner/app/mcp_server.py`

Tools:

- `generate_revenue_plan(payload)` -> returns a staged, redundant revenue plan with guardrails
- `assess_strategy_risk(summary, tactics)` -> flags risky or disallowed tactics and suggests compliant replacements
- `list_safe_revenue_tracks()` -> returns built-in revenue track definitions
- `revenue_plan_request_schema()` / `revenue_plan_response_schema()` -> JSON schema helpers

Run it:

```bash
cd services/revenue_planner
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.mcp_server
```

