# Autonomous Listing Service — Mission Diary

> Tracks iterations as the service and the agency co-develop, per Section 15 of `autonomous_super_agency.md`.

## 2025-12-10 — Sprint 0 Kickoff
- Captured the end-to-end technical blueprint (`docs/autonomous_listing_service.md`), including AI pipeline, marketplace strategy, and UI/UX plan.
- Introduced the iterative improvement protocol (Section 11 of same doc) to bind this mission to the broader agency.
- Scaffolded the FastAPI MVP (`services/autonomous_listing/`) with placeholder pipelines for image enhancement, copywriting, and publishing so the request→response loop is testable.
- Added Dockerfile + README quick start to unblock sandbox deployment.

### Metrics / Signals
- Endpoint latency (local): ~300ms end-to-end with stubbed async steps.
- Coverage: supports multiple target platforms in schema; pipeline still simulated.

### Next Focus
- Replace stub pipelines with actual AI services (vision enhancer, LLM copywriter, marketplace adapters).
- Instrument telemetry + logging hooks to feed Agency-wide reports.
- Stand up sandbox deployment and run first end-to-end seller simulations.

## 2025-12-10 — Telemetry Hook-up
- Implemented JSONL telemetry sink (`app/services/telemetry.py`) with configurable path.
- Wired orchestrator events: request receipt, image enhancement, copy generation, publication trigger, and response ready (duration + platform metrics).
- README now documents telemetry output and env override.

### Metrics / Signals
- Average stubbed flow duration still sub-second; telemetry introduces negligible overhead.
- Log location: `/workspace/logs/listings/events.log` (dev env default).

### Next Focus
- Feed telemetry data into dashboards / mission retros.
- Instrument mission diary hooks + improvement backlog automation when submitting deploys.

## 2025-12-10 — AI Pipeline & Marketplace Skeleton
- Added configurable settings + clients for OpenAI (LLM) and external vision service (ESRGAN/background removal endpoint stubs).
- Description generator now calls LLM client with optional RAG snippets; vision enhancer defers to `VisionClient`.
- Marketplace architecture implemented with adapter interface plus Craigslist (Playwright/email flow placeholder) and Mercari (API) adapters.
- Channel publisher now aggregates adapter responses, emitting per-platform status + notes.

### Metrics / Signals
- Response time increased slightly (~450ms locally) due to network-ready clients; still sub-second.
- Missing adapter or credentials are surfaced in response notes, enabling quick remediation.

### Next Focus
- Flesh out Nextdoor/OfferUp adapters and tie telemetry into mission dashboards.
- Begin engagement hub design for unified buyer messaging.
