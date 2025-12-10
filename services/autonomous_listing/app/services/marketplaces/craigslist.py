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
        # Placeholder: in production use Playwright + email confirmation workflow.
        await asyncio.sleep(0.2)
        status = "pending"
        message = (
            "Awaiting manual confirmation email."
            if not self._reply_email
            else "Submission queued; confirmation will be sent to configured email."
        )
        return PublicationResult(
            platform=self.platform,
            status=status,
            reference_id=f"CL-{listing_id[:8]}",
            message=message,
        )
