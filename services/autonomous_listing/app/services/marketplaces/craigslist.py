from __future__ import annotations

import asyncio
from typing import List

from ... import schemas
from ..config import get_settings
from .base import MarketplacePublisher, PublicationResult


class CraigslistPublisher(MarketplacePublisher):
    platform = schemas.PlatformEnum.craigslist

    def __init__(self) -> None:
        self._reply_email = get_settings().craigslist_email

    async def publish(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        description: str,
        recommended_price: float,
        enhanced_assets: List[str],
    ) -> PublicationResult:
        # Assisted publish: return a ready-to-post package + instructions.
        # (Full automation is intentionally not enabled by default because Craigslist flows
        # often require email confirmation and may include anti-bot checks.)
        await asyncio.sleep(0.2)
        status = "pending"
        message = "Craigslist posting package generated; manual posting/confirmation required."

        # Craigslist title length guidance is strict-ish; keep it compact.
        title = (request.title_hint or request.brand or request.category or "Listing").strip()
        if len(title) > 70:
            title = title[:67].rstrip() + "..."

        package = {
            "platform": "craigslist",
            "title": title,
            "price": recommended_price,
            "location": request.location,
            "body": description,
            "images": enhanced_assets,
            "reply_email": self._reply_email,
            "assisted_posting_steps": [
                "Open Craigslist for your region and start a new post.",
                "Choose the closest category for the item/event.",
                "Paste the title and body exactly; verify facts and condition are accurate.",
                "Set price and location; choose pickup/shipping options if offered.",
                "Upload images in the provided order (hero image first).",
                "Complete any verification (phone/email) and publish.",
                "If an email confirmation is sent, confirm using the configured reply email.",
            ],
        }
        return PublicationResult(
            platform=self.platform,
            status=status,
            reference_id=f"CL-{listing_id[:8]}",
            message=message,
            data=package,
        )
