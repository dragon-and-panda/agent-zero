from __future__ import annotations

import asyncio
from typing import List

import httpx

from ... import schemas
from ..config import get_settings
from .base import MarketplacePublisher, PublicationResult


class MercariPublisher(MarketplacePublisher):
    platform = schemas.PlatformEnum.mercari

    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.mercari_api_key
        self._client = httpx.AsyncClient(timeout=20) if self._api_key else None

    async def publish(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        description: str,
        recommended_price: float,
        enhanced_assets: List[str],
    ) -> PublicationResult:
        if not self._client:
            await asyncio.sleep(0.1)
            return PublicationResult(
                platform=self.platform,
                status="pending",
                message="Mercari API key missing; queued for manual posting.",
            )

        payload = {
            "title": request.title_hint or f"{request.category} listing",
            "description": description,
            "price": recommended_price,
            "category": request.category,
            "location": request.location,
            "photos": enhanced_assets,
        }
        resp = await self._client.post(
            "https://api.mercari.com/listings",
            json=payload,
            headers={"Authorization": f"Bearer {self._api_key}"},
        )
        if resp.status_code >= 400:
            return PublicationResult(
                platform=self.platform,
                status="failed",
                message=f"Mercari API error: {resp.text}",
            )
        data = resp.json()
        return PublicationResult(
            platform=self.platform,
            status="live",
            reference_id=data.get("id"),
            message="Listing live on Mercari.",
        )
