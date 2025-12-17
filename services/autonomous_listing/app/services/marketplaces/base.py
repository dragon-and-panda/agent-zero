from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import List, Optional

from ... import schemas


@dataclass
class PublicationResult:
    platform: schemas.PlatformEnum
    status: str  # "pending" | "live" | "failed"
    reference_id: Optional[str] = None
    message: Optional[str] = None
    data: dict | None = None


class MarketplacePublisher(abc.ABC):
    platform: schemas.PlatformEnum

    @abc.abstractmethod
    async def publish(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        description: str,
        recommended_price: float,
        enhanced_assets: List[str],
    ) -> PublicationResult:
        ...
