from __future__ import annotations

import asyncio
import random
from typing import List, Tuple

import httpx

from ... import schemas
from ..config import get_settings
from ..llm_client import LLMClient


class DescriptionGenerator:
    """
    Generates marketing copy using an LLM + optional RAG endpoint for contextual snippets.
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
    ) -> Tuple[str, float]:
        references = await self._retrieve_references(request)
        prompt = self._build_prompt(request, enhanced_assets)
        narrative = await self._llm.generate_marketing_copy(prompt, references)

        suggested_price = request.preferences.target_price or round(
            random.uniform(20, 200), 2
        )

        return narrative.strip(), suggested_price

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

    def _build_prompt(
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

        return (
            f"{hero_line}\n"
            f"Category: {request.category}\n"
            f"Location: {request.location}\n"
            f"Desired tone: {tone}\n"
            f"Target platforms: {platforms}\n"
            f"Seller notes: {request.raw_description}\n"
            f"{bullet}"
        )
