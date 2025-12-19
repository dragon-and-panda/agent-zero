from __future__ import annotations

import asyncio
from typing import List

from ... import schemas
from ..config import get_settings
from .base import MarketplacePublisher, PublicationResult


class MercariPublisher(MarketplacePublisher):
    platform = schemas.PlatformEnum.mercari

    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.mercari_api_key

    async def publish(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        description: str,
        recommended_price: float,
        enhanced_assets: List[str],
    ) -> PublicationResult:
        # Assisted publish: return a ready-to-post package + instructions.
        # (Mercari automation is intentionally not enabled by default; stable official APIs vary by region/account.)
        await asyncio.sleep(0.1)

        title = (request.title_hint or request.brand or request.category or "Listing").strip()
        if len(title) > 80:
            title = title[:77].rstrip() + "..."

        package = {
            "platform": "mercari",
            "title": title,
            "price": recommended_price,
            "category_hint": request.category,
            "description": description,
            "photos": enhanced_assets,
            "condition_hint": request.condition,
            "shipping_hint": "shipping" if not request.preferences.pickup_only else "local pickup",
            "assisted_posting_steps": [
                "Open Mercari and tap Sell.",
                "Upload photos (hero first), then confirm crop/rotation.",
                "Paste the title and description; verify facts and condition are accurate.",
                "Choose the closest category and condition.",
                "Set price; decide on offers/negotiation preferences.",
                "Configure shipping vs local pickup as appropriate.",
                "List the item and verify it appears correctly.",
            ],
            "api_key_configured": bool(self._api_key),
        }

        msg = (
            "Mercari posting package generated; manual posting recommended."
            if not self._api_key
            else "Mercari posting package generated (API key present, but still using assisted mode)."
        )
        return PublicationResult(
            platform=self.platform,
            status="pending",
            reference_id=f"ME-{listing_id[:8]}",
            message=msg,
            data=package,
        )
