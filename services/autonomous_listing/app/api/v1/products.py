from __future__ import annotations

import asyncio
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from ... import schemas
from ...services.agents.orchestrator import DropshipOrchestrator
from ...services.product_research import ProductResearcher
from ...services.scrapers.playwright_scraper import scrape_product_page

router = APIRouter(prefix="/v1/products", tags=["products"])

# In-memory task state for local/dev runtime.
# Can be swapped with Redis/Celery without changing public API.
task_store: Dict[str, Dict[str, Any]] = {}


class ProductResearchRequest(BaseModel):
    niche: str
    max_price: float | None = 50.0
    min_margin: float = 0.3
    target_country: str = "US"
    max_results: int = 10


class GeneratedListing(BaseModel):
    title: str
    description: str
    variants: List[dict]
    price_suggestion: float
    tags: List[str]
    confidence_score: float
    source_url: str
    supplier_data: dict
    images: List[str]


class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: float
    result: List[GeneratedListing] | None = None
    error: str | None = None


def _to_internal_research_request(req: ProductResearchRequest) -> schemas.ProductResearchRequest:
    constraints: list[str] = []
    if req.max_price is not None:
        constraints.append(f"max_buy_price:{req.max_price}")
    constraints.append(f"min_margin:{req.min_margin}")
    constraints.append(f"target_country:{req.target_country}")
    return schemas.ProductResearchRequest(
        niche=req.niche,
        budget_max=req.max_price,
        goals=["high_margin", "fast_sell"],
        constraints=constraints,
        max_results=req.max_results,
    )


async def _run_product_research(task_id: str, req: ProductResearchRequest) -> None:
    try:
        task_store[task_id]["status"] = "running"
        task_store[task_id]["progress"] = 10.0

        internal_req = _to_internal_research_request(req)
        researcher = ProductResearcher()
        research_result = await asyncio.to_thread(researcher.research, internal_req)
        task_store[task_id]["progress"] = 60.0

        orchestrator = DropshipOrchestrator()
        listings: list[dict[str, Any]] = []
        for candidate in research_result.candidates:
            raw_data = {
                "source_url": candidate.evidence_links[0] if candidate.evidence_links else "",
                "title": candidate.title,
                "description": candidate.why,
                "images": [],
                "supplier_data": {
                    "candidate_score": candidate.score,
                    "risks": candidate.risks,
                    "keywords": candidate.keywords,
                    "suggested_next_step": candidate.suggested_next_step,
                },
            }
            listing = await orchestrator.generate_single_listing(raw_data)
            listing["confidence_score"] = round(min(0.98, candidate.score / 100.0), 2)
            listings.append(listing)

        task_store[task_id]["status"] = "completed"
        task_store[task_id]["progress"] = 100.0
        task_store[task_id]["result"] = listings
    except Exception as exc:
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["error"] = str(exc)
        task_store[task_id]["progress"] = 100.0


@router.post("/research", response_model=dict)
async def research_products(req: ProductResearchRequest) -> dict:
    """Trigger full research workflow and return a task_id for polling."""
    task_id = str(uuid4())
    task_store[task_id] = {
        "status": "pending",
        "progress": 0.0,
        "result": None,
        "error": None,
        "request": req.model_dump(),
    }

    asyncio.create_task(_run_product_research(task_id, req))
    return {"task_id": task_id, "status": "queued"}


@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_result(task_id: str) -> TaskStatus:
    """Poll for task progress and final generated listings."""
    task_data = task_store.get(task_id)
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskStatus(
        task_id=task_id,
        status=task_data["status"],
        progress=task_data["progress"],
        result=task_data["result"],
        error=task_data["error"],
    )


@router.post("/listings/generate", response_model=GeneratedListing)
async def generate_listing(product_url: HttpUrl) -> GeneratedListing:
    """One-shot: scrape -> analyze -> generate optimized listing."""
    try:
        raw_data = await scrape_product_page(str(product_url))
        if not raw_data:
            raise HTTPException(status_code=400, detail="Failed to scrape product page")

        orchestrator = DropshipOrchestrator()
        listing = await orchestrator.generate_single_listing(raw_data)
        return GeneratedListing(**listing)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

