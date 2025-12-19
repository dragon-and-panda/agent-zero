"""
Autonomous Listing MCP Server

Exposes the existing listing orchestrator as MCP tools over stdio by default.
"""

from __future__ import annotations

from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from . import schemas
from .services.orchestrator import ListingOrchestrator
from .services.pipelines.description_generator import DescriptionGenerator
from .services.pipelines.image_enhancer import ImageEnhancer
from .services.pipelines.publisher import ChannelPublisher
from .services.perception import PerceptionEngine
from .services.telemetry import TelemetryClient
from .services.intake_template import listing_intake_template
from .services.product_research import ProductResearcher
from .services.storage import ListingStore

mcp = FastMCP("autonomous-listing")

_orchestrator = ListingOrchestrator(
    enhancer=ImageEnhancer(),
    copywriter=DescriptionGenerator(),
    publisher=ChannelPublisher(),
    perception=PerceptionEngine(),
    telemetry=TelemetryClient(),
)


@mcp.tool()
def list_supported_platforms() -> List[str]:
    """Return the set of known marketplace platform identifiers."""
    return [p.value for p in schemas.PlatformEnum]


@mcp.tool()
def listing_request_schema() -> Dict[str, Any]:
    """JSON schema for the listing request payload."""
    return schemas.ListingRequest.model_json_schema()


@mcp.tool()
def listing_response_schema() -> Dict[str, Any]:
    """JSON schema for the listing response payload."""
    return schemas.ListingResponse.model_json_schema()


@mcp.tool()
def validate_listing_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate/normalize a listing request.

    Returns the validated payload (with defaults applied) as a plain dict.
    """
    req = schemas.ListingRequest.model_validate(payload)
    return req.model_dump(mode="json")


@mcp.tool()
def get_listing_intake_template(
    platforms: List[str] | None = None, listing_type: str = "item"
) -> Dict[str, Any]:
    """
    Returns a fill-in template for the user (including photo slots) and a mock preview for the primary platform.
    """
    return listing_intake_template(platforms=platforms, listing_type=listing_type)


@mcp.tool()
def research_products(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Minimal product discovery tool for dropshipping/sourcing.
    Input: ProductResearchRequest-compatible JSON.
    """
    req = schemas.ProductResearchRequest.model_validate(payload)
    res = ProductResearcher().research(req)
    return res.model_dump(mode="json")


@mcp.tool()
async def create_listing(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a listing via the existing orchestrator pipeline.

    Input: ListingRequest-compatible JSON object.
    Output: ListingResponse as JSON.
    """
    req = schemas.ListingRequest.model_validate(payload)
    res = await _orchestrator.create_listing(req, publish=True)
    return res.model_dump(mode="json")


@mcp.tool()
async def create_listing_draft(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Draft-only: generates enhanced assets + master copy + platform variants + quality scoring,
    and skips marketplace publication.
    """
    req = schemas.ListingRequest.model_validate(payload)
    res = await _orchestrator.create_listing(req, publish=False)
    return res.model_dump(mode="json")


@mcp.tool()
async def create_craigslist_posting_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience tool: generate a draft and return only the Craigslist posting package
    (title/price/body/images + assisted steps).
    """
    req = schemas.ListingRequest.model_validate(payload)
    res = await _orchestrator.create_listing(req, publish=True)
    pub = res.platform_publication.get("craigslist", {})
    return {
        "listing_id": res.status.listing_id,
        "selected_title": res.selected_title,
        "recommended_price": res.recommended_price,
        "verified_attributes": res.verified_attributes,
        "craigslist": pub.get("data", {}),
        "status": pub.get("status"),
        "message": pub.get("message"),
    }


@mcp.tool()
async def extract_verified_attributes(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run multi-source perception + redundant verification and return verified attributes.
    """
    req = schemas.ListingRequest.model_validate(payload)
    engine = PerceptionEngine()
    verified, report = await engine.infer_verified_attributes(request=req)
    return {"verified_attributes": verified, "perception_report": report}


@mcp.tool()
def get_listing(listing_id: str) -> Dict[str, Any]:
    store = ListingStore()
    row = store.get_listing(listing_id)
    if not row:
        return {"error": "Listing not found", "listing_id": listing_id}
    return {
        "listing_id": row.listing_id,
        "owner_id": row.owner_id,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "request": row.request,
        "response": row.response,
    }


@mcp.tool()
def list_listings(owner_id: str | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    store = ListingStore()
    rows = store.list_listings(owner_id=owner_id, limit=limit)
    return [
        {
            "listing_id": r.listing_id,
            "owner_id": r.owner_id,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "request": r.request,
            "response": r.response,
        }
        for r in rows
    ]


@mcp.tool()
def list_publish_jobs(status: str | None = "needs_human", platform: str | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    store = ListingStore()
    jobs = store.list_publish_jobs(status=status, platform=platform, limit=limit)
    return [
        {
            "job_id": j.job_id,
            "listing_id": j.listing_id,
            "platform": j.platform,
            "mode": j.mode,
            "status": j.status,
            "created_at": j.created_at,
            "updated_at": j.updated_at,
            "payload": j.payload,
            "result": j.result,
        }
        for j in jobs
    ]


@mcp.tool()
def mark_publish_job_posted(job_id: str, posted_url: str | None = None, reference_id: str | None = None, notes: str | None = None) -> Dict[str, Any]:
    store = ListingStore()
    job = store.mark_job_posted(job_id=job_id, posted_url=posted_url, reference_id=reference_id, notes=notes)
    if not job:
        return {"error": "Publish job not found", "job_id": job_id}
    return {
        "job_id": job.job_id,
        "listing_id": job.listing_id,
        "platform": job.platform,
        "mode": job.mode,
        "status": job.status,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "payload": job.payload,
        "result": job.result,
    }


def main() -> None:
    # Default transport is stdio, which is what most MCP clients expect.
    mcp.run()


if __name__ == "__main__":
    main()

