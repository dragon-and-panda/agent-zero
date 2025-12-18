from fastapi import FastAPI, HTTPException

from . import schemas
from .services.intake_template import listing_intake_template
from .services.product_research import ProductResearcher
from .services.orchestrator import ListingOrchestrator
from .services.pipelines.description_generator import DescriptionGenerator
from .services.pipelines.image_enhancer import ImageEnhancer
from .services.pipelines.publisher import ChannelPublisher
from .services.storage import ListingStore
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
    storage=ListingStore(),
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


@app.post("/research/products", response_model=schemas.ProductResearchResponse)
async def research_products(payload: schemas.ProductResearchRequest) -> schemas.ProductResearchResponse:
    """
    Minimal product discovery endpoint for sourcing/dropshipping.
    """
    return ProductResearcher().research(payload)


@app.post("/listings", response_model=schemas.ListingResponse)
async def create_listing(payload: schemas.ListingRequest) -> schemas.ListingResponse:
    """
    Entry point for creating a new autonomous listing.
    Downstream pipelines are mocked for now and should be replaced with actual AI services.
    """

    return await orchestrator.create_listing(payload, publish=True)


@app.post("/listings/draft", response_model=schemas.ListingResponse)
async def create_listing_draft(payload: schemas.ListingRequest) -> schemas.ListingResponse:
    """
    Draft-only entry point: generates enhanced assets + best-in-class copy + variants + scoring,
    but does not publish to marketplaces.
    """
    return await orchestrator.create_listing(payload, publish=False)


@app.get("/listings/{listing_id}", response_model=schemas.StoredListing)
async def get_listing(listing_id: str) -> schemas.StoredListing:
    store = ListingStore()
    row = store.get_listing(listing_id)
    if not row:
        raise HTTPException(status_code=404, detail="Listing not found")
    return schemas.StoredListing(
        listing_id=row.listing_id,
        owner_id=row.owner_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
        request=row.request,
        response=row.response,
    )


@app.get("/listings", response_model=list[schemas.StoredListing])
async def list_listings(owner_id: str | None = None, limit: int = 50) -> list[schemas.StoredListing]:
    store = ListingStore()
    rows = store.list_listings(owner_id=owner_id, limit=limit)
    return [
        schemas.StoredListing(
            listing_id=r.listing_id,
            owner_id=r.owner_id,
            created_at=r.created_at,
            updated_at=r.updated_at,
            request=r.request,
            response=r.response,
        )
        for r in rows
    ]


@app.get("/publish/jobs", response_model=list[schemas.PublishJob])
async def list_publish_jobs(
    status: str | None = "needs_human",
    platform: str | None = None,
    limit: int = 50,
) -> list[schemas.PublishJob]:
    store = ListingStore()
    jobs = store.list_publish_jobs(status=status, platform=platform, limit=limit)
    return [
        schemas.PublishJob(
            job_id=j.job_id,
            listing_id=j.listing_id,
            platform=j.platform,
            mode=j.mode,
            status=j.status,
            created_at=j.created_at,
            updated_at=j.updated_at,
            payload=j.payload,
            result=j.result,
        )
        for j in jobs
    ]


@app.post("/publish/jobs/{job_id}/mark_posted", response_model=schemas.PublishJob)
async def mark_job_posted(job_id: str, payload: schemas.MarkPostedRequest) -> schemas.PublishJob:
    store = ListingStore()
    job = store.mark_job_posted(
        job_id=job_id,
        posted_url=payload.posted_url,
        reference_id=payload.reference_id,
        notes=payload.notes,
    )
    if not job:
        raise HTTPException(status_code=404, detail="Publish job not found")
    return schemas.PublishJob(
        job_id=job.job_id,
        listing_id=job.listing_id,
        platform=job.platform,
        mode=job.mode,
        status=job.status,
        created_at=job.created_at,
        updated_at=job.updated_at,
        payload=job.payload,
        result=job.result,
    )
