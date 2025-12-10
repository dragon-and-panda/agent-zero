from __future__ import annotations

import asyncio
from typing import List

from ... import schemas
from ..vision_client import VisionClient


class ImageEnhancer:
    """
    Orchestrates the external vision client with graceful fallbacks.
    """

    def __init__(self, vision_client: VisionClient | None = None) -> None:
        self._vision = vision_client or VisionClient()

    async def process(
        self, listing_id: str, assets: List[schemas.ListingAsset]
    ) -> List[str]:
        return await self._vision.enhance_assets(listing_id, assets)
