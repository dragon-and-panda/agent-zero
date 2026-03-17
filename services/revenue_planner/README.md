# Revenue Planner Service

This service provides a deterministic, compliance-aware planning layer for autonomous revenue missions. It is intentionally designed to favor:

- first-party, opt-in lead generation
- productized services, digital products, marketplaces, and educational content
- redundancy, contingency planning, and channel concentration controls

It explicitly rejects risky patterns such as harvested-contact monetization, inbox scraping, and spam-oriented outreach.

## Quick Start

```bash
cd services/revenue_planner
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run as an MCP Server

```bash
cd services/revenue_planner
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.mcp_server
```

## API Endpoints

- `GET /health` -> service health status
- `GET /tracks` -> built-in safe revenue tracks
- `GET /plans/schema` -> JSON schema for request payloads
- `POST /plans` -> generate a staged revenue plan
- `POST /assess-risk` -> inspect proposed tactics for risk and disallowed patterns

## Example Plan Request

```json
{
  "mission_name": "cash-flow launch",
  "cash_on_hand": 150,
  "weekly_hours": 12,
  "skills": ["automation", "writing", "research"],
  "existing_assets": ["github", "website", "newsletter"],
  "preferred_tracks": ["productized_service", "digital_product"],
  "proposed_tactics": ["sell email lists", "launch an automation audit offer"],
  "constraints": ["no paid ads"],
  "automation_maturity": "high",
  "risk_tolerance": "low",
  "audience_size": 300
}
```

The response includes:

- hard guardrails
- rejected tactics and compliant replacements
- two primary tracks plus a backup track
- phase-by-phase next actions
- contingency rules and KPI targets
