from fastapi import FastAPI

from . import schemas
from .services.intake_template import listing_intake_template
from .services.orchestrator import ListingOrchestrator
from .services.pipelines.description_generator import DescriptionGenerator
from .services.pipelines.image_enhancer import ImageEnhancer
from .services.pipelines.publisher import ChannelPublisher
from .services.telemetry import TelemetryClient

app = FastAPI(
    title="Autonomous Listing Service",
    description="Transforms seller inputs into multi-channel listings via AI pipelines.",
    version="0.1.0",
)

orchestrator = ListingOrchestrator(
    enhancer=ImageEnhancer(),
    copywriter=DescriptionGenerator(),
    publisher=ChannelPublisher(),
    # perception defaults to PerceptionEngine() (vision+search redundancy)
    telemetry=TelemetryClient(),
)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.get("/listings/template")
async def get_listing_template(
    platforms: str | None = None, listing_type: str = "item"
) -> dict:
    """
    Returns a fill-in JSON template + platform checklist + mock preview.

    Query params:
    - platforms: comma-separated platform ids (e.g. "craigslist,mercari")
    - listing_type: item | event | service
    """
    platform_list = [p.strip() for p in (platforms or "").split(",") if p.strip()] or None
    return listing_intake_template(platforms=platform_list, listing_type=listing_type)


@app.post("/listings", response_model=schemas.ListingResponse)
async def create_listing(payload: schemas.ListingRequest) -> schemas.ListingResponse:
    """
    Entry point for creating a new autonomous listing.
    Downstream pipelines are mocked for now and should be replaced with actual AI services.
    """

    return await orchestrator.create_listing(payload)


@app.post("/listings/draft", response_model=schemas.ListingResponse)
async def create_listing_draft(payload: schemas.ListingRequest) -> schemas.ListingResponse:
    """
    Draft-only entry point: generates enhanced assets + best-in-class copy + variants + scoring,
    but does not publish to marketplaces.
    """
    # Minimal approach for now: reuse the full orchestrator but set target_platforms empty to skip publication.
    draft_payload = payload.model_copy(update={"target_platforms": []})
    return await orchestrator.create_listing(draft_payload)
