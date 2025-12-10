from __future__ import annotations

import asyncio
from typing import List

import httpx

from ..config import get_settings
from .. import schemas


class VisionClient:
    """
    Handles communication with external vision pipeline (e.g., internal GPU service).
    Falls back to simulated enhancements when API credentials are absent.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self._api_base = settings.vision_api_base
        self._api_key = settings.vision_api_key
        self._client = httpx.AsyncClient(timeout=30) if self._api_base else None

    async def enhance_assets(
        self, listing_id: str, assets: List[schemas.ListingAsset]
    ) -> List[str]:
        if not assets:
            return []

        if not self._client:
            await asyncio.sleep(0.1)
            return [
                asset.source_uri or f"s3://placeholder/{listing_id}/{idx}.jpg"
                for idx, asset in enumerate(assets)
            ]

        payload = {
            "listing_id": listing_id,
            "assets": [
                {"source_uri": asset.source_uri, "caption": asset.caption}
                for asset in assets
            ],
        }
        resp = await self._client.post(
            f"{self._api_base}/enhance",
            json=payload,
            headers={"Authorization": f"Bearer {self._api_key}"},
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("enhanced_uris", [])
