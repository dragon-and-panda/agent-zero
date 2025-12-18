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
    res = await _orchestrator.create_listing(req)
    return res.model_dump(mode="json")


@mcp.tool()
async def create_listing_draft(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Draft-only: generates enhanced assets + master copy + platform variants + quality scoring,
    and skips marketplace publication.
    """
    req = schemas.ListingRequest.model_validate(payload)
    draft_req = req.model_copy(update={"target_platforms": []})
    res = await _orchestrator.create_listing(draft_req)
    return res.model_dump(mode="json")


@mcp.tool()
async def create_craigslist_posting_package(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience tool: generate a draft and return only the Craigslist posting package
    (title/price/body/images + assisted steps).
    """
    req = schemas.ListingRequest.model_validate(payload)
    res = await _orchestrator.create_listing(req)
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


def main() -> None:
    # Default transport is stdio, which is what most MCP clients expect.
    mcp.run()


if __name__ == "__main__":
    main()

