from __future__ import annotations

import asyncio
from dataclasses import dataclass
import random
from typing import Dict, List, Tuple

import httpx

from ... import schemas
from ..config import get_settings
from ..llm_client import LLMClient


@dataclass
class CopyPackage:
    master_description: str
    suggested_price: float
    platform_variants: Dict[str, str]
    quality_report: dict


class DescriptionGenerator:
    """
    Generates high-quality marketing copy using an LLM + optional RAG endpoint.
    Produces a master description plus platform-specific variants and a rubric score.
    """

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self._llm = llm_client or LLMClient()
        self._rag_endpoint = get_settings().marketing_rag_endpoint
        self._rag_client = httpx.AsyncClient(timeout=10) if self._rag_endpoint else None

    async def generate(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        enhanced_assets: List[str],
    ) -> CopyPackage:
        references = await self._retrieve_references(request)
        master_prompt = self._build_master_prompt(request, enhanced_assets)
        master = await self._llm.generate_marketing_copy(master_prompt, references)

        suggested_price = request.preferences.target_price or round(
            random.uniform(20, 200), 2
        )

        checklist = self._rubric_checklist(request)
        context = self._critique_context(request, enhanced_assets, suggested_price)
        quality = await self._llm.critique_and_score(
            draft=master.strip(), checklist=checklist, context=context
        )

        # If score is low, do one rewrite pass.
        if isinstance(quality, dict) and quality.get("score", 0) < 80:
            rewrite_prompt = self._build_rewrite_prompt(
                request=request,
                enhanced_assets=enhanced_assets,
                suggested_price=suggested_price,
                critique=quality,
            )
            master = await self._llm.generate_marketing_copy(rewrite_prompt, references)
            quality = await self._llm.critique_and_score(
                draft=master.strip(), checklist=checklist, context=context
            )

        variants = await self._generate_platform_variants(
            request=request,
            master=master.strip(),
            enhanced_assets=enhanced_assets,
            suggested_price=suggested_price,
            references=references,
        )

        return CopyPackage(
            master_description=master.strip(),
            suggested_price=suggested_price,
            platform_variants=variants,
            quality_report=quality if isinstance(quality, dict) else {"raw": quality},
        )

    async def _retrieve_references(
        self, request: schemas.ListingRequest
    ) -> List[str]:
        if not self._rag_client:
            return []

        payload = {
            "category": request.category,
            "notes": request.raw_description,
            "location": request.location,
        }
        resp = await self._rag_client.post(str(self._rag_endpoint), json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("snippets", [])

    def _build_master_prompt(
        self, request: schemas.ListingRequest, enhanced_assets: List[str]
    ) -> str:
        hero_line = request.title_hint or "Craft a standout listing title"
        bullet = (
            f"Photos: {len(enhanced_assets)} enhanced shots available."
            if enhanced_assets
            else "Photos still processing."
        )
        tone = request.preferences.tone or "approachable premium"
        platforms = ", ".join([p.value for p in request.target_platforms])

        listing_type = request.listing_type or "item"
        brand = f"Brand/Organizer: {request.brand}\n" if request.brand else ""
        condition = f"Condition: {request.condition}\n" if request.condition else ""
        dims = f"Dimensions: {request.dimensions}\n" if request.dimensions else ""
        delivery = f"Delivery/Fulfillment: {request.delivery}\n" if request.delivery else ""
        event_bits = ""
        if listing_type == "event":
            when = f"When: {request.event_datetime}\n" if request.event_datetime else ""
            dur = f"Duration: {request.event_duration}\n" if request.event_duration else ""
            event_bits = when + dur

        structure = (
            "Output a single master listing description with:\n"
            "1) 3-6 title options\n"
            "2) A punchy opening\n"
            "3) Scannable bullets (features/what’s included)\n"
            "4) Condition/details (only truthful)\n"
            "5) Logistics (pickup/shipping, location, timing)\n"
            "6) A friendly call-to-action\n"
            "Keep it highly professional and conversion-focused."
        )

        return (
            f"{structure}\n\n"
            f"Title hint: {hero_line}\n"
            f"Listing type: {listing_type}\n"
            f"Category: {request.category}\n"
            f"Location: {request.location}\n"
            f"Desired tone: {tone}\n"
            f"Target platforms: {platforms}\n"
            f"{brand}{condition}{dims}{delivery}{event_bits}"
            f"Seller notes: {request.raw_description}\n"
            f"{bullet}"
        )

    def _rubric_checklist(self, request: schemas.ListingRequest) -> List[str]:
        base = [
            "Specificity: includes concrete details, not vague hype",
            "Truthfulness: no unverifiable claims, no invented specs",
            "Scannability: clear sections and bullets",
            "Logistics: location + pickup/shipping/delivery clarity",
            "CTA: friendly, low-friction next step",
        ]
        if request.listing_type == "event":
            base.append("Event clarity: what/when/where and what to expect")
        return base

    def _critique_context(
        self,
        request: schemas.ListingRequest,
        enhanced_assets: List[str],
        suggested_price: float,
    ) -> str:
        return (
            f"type={request.listing_type}, category={request.category}, "
            f"location={request.location}, assets={len(enhanced_assets)}, "
            f"price_hint={suggested_price}"
        )

    def _build_rewrite_prompt(
        self,
        request: schemas.ListingRequest,
        enhanced_assets: List[str],
        suggested_price: float,
        critique: dict,
    ) -> str:
        notes = "\n- ".join([str(x) for x in critique.get("rewrite_notes", [])])
        return (
            "Rewrite the listing to address the critique notes below.\n"
            "Keep it truthful, premium, and highly conversion-focused.\n"
            "Return the full improved master listing (same structure).\n\n"
            f"Critique notes:\n- {notes}\n\n"
            f"Key facts:\n"
            f"Type: {request.listing_type}\n"
            f"Category: {request.category}\n"
            f"Location: {request.location}\n"
            f"Condition: {request.condition}\n"
            f"Brand: {request.brand}\n"
            f"Dimensions: {request.dimensions}\n"
            f"Delivery: {request.delivery}\n"
            f"Event datetime: {request.event_datetime}\n"
            f"Event duration: {request.event_duration}\n"
            f"Suggested price: {suggested_price}\n"
            f"Photo count: {len(enhanced_assets)}\n"
            f"Seller notes: {request.raw_description}\n"
        )

    async def _generate_platform_variants(
        self,
        request: schemas.ListingRequest,
        master: str,
        enhanced_assets: List[str],
        suggested_price: float,
        references: List[str],
    ) -> Dict[str, str]:
        variants: Dict[str, str] = {}
        # For MVP: generate variants only for requested platforms.
        for platform in request.target_platforms:
            style = self._platform_style(platform.value)
            if not style:
                continue
            prompt = (
                "Create a platform-specific listing description variant.\n"
                "Rules:\n"
                "- Keep all facts consistent with the master.\n"
                "- Optimize for the platform constraints and buyer expectations.\n"
                "- Do not mention other platforms.\n\n"
                f"Platform: {platform.value}\n"
                f"Style guide: {style}\n"
                f"Suggested price: {suggested_price}\n"
                f"Location: {request.location}\n"
                f"Master:\n{master}\n"
            )
            text = await self._llm.generate_marketing_copy(prompt, references)
            variants[platform.value] = text.strip()
        return variants

    def _platform_style(self, platform: str) -> str:
        # Tight, opinionated style guides.
        guides = {
            "craigslist": "Direct, local, minimal fluff. Clear condition + pickup details. Short paragraphs + bullets.",
            "offerup": "Mobile-first. Short punchy lines, emojis avoided, strong CTA, highlight top 3 benefits fast.",
            "nextdoor": "Neighborly tone. Trust/safety, local pickup window, polite CTA.",
            "mercari": "Ecommerce-style. Condition grading, what’s included, shipping/pickup clarity, avoid hype.",
            "poshmark": "Fashion-first. Brand/size/condition upfront, style keywords, bundle-friendly CTA.",
            "etsy": "SEO tags/materials/story. Handmade/vintage/supplies language, dimensions/materials, care notes.",
            "shopify": "Premium product page sections: Overview, Details, Shipping/Returns, FAQ. SEO-friendly headings.",
        }
        return guides.get(platform, "")
