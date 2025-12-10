# Autonomous Listing Service — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Integrate real image enhancement pipeline (ESRGAN + background removal) with object storage outputs | Vision Stylist | Vision client + API hooks scaffolded; need GPU infra + storage wiring |
| P0 | Wire Copywriter agent to GPT-4o + marketing RAG corpus | Listing Copywriter | LLM client + RAG endpoint hooks live; expand corpus + prompt tuning |
| P1 | Implement MarketplacePublisher adapters for Craigslist (Playwright) and Mercari (API) | Channel Publisher | Base adapters live (email/Playwright placeholder + API). Extend to full automation |
| P1 | Add telemetry + mission diary hooks directly in orchestrator to log latency, cost, and platform outcomes | Telemetry Sentinel | JSONL sink in place; next wire into dashboards + mission retros |
| P2 | Build Engagement Hub stub (WebSocket + AI suggested replies) | Buyer Liaison | Required for unified messaging experience |
| P2 | Containerize sandbox deployment with IaC + scheduled smoke tests | Lifecycle Steward | Ensures reliable rollout path |
