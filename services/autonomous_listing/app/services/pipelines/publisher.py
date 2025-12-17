from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, List

from ... import schemas
from ..orchestrator import PublishResult
from .marketplaces.base import MarketplacePublisher, PublicationResult
from .marketplaces.craigslist import CraigslistPublisher
from .marketplaces.mercari import MercariPublisher


class ChannelPublisher:
    """
    Coordinates marketplace-specific adapters.
    Defaults to pending/manual state when an adapter doesn't exist yet.
    """

    def __init__(self, adapters: List[MarketplacePublisher] | None = None) -> None:
        adapters = adapters or [
            CraigslistPublisher(),
            MercariPublisher(),
        ]
        self._registry: Dict[schemas.PlatformEnum, MarketplacePublisher] = {
            adapter.platform: adapter for adapter in adapters
        }

    async def schedule_publication(
        self,
        listing_id: str,
        request: schemas.ListingRequest,
        enhanced_assets: List[str],
        master_description: str,
        platform_variants: Dict[str, str] | None,
        recommended_price: float,
    ) -> PublishResult:
        confirmed: List[schemas.PlatformEnum] = []
        failed: List[schemas.PlatformEnum] = []
        pending = False
        notes_parts: List[str] = []
        platform_results: Dict[str, dict] = {}

        for platform in request.target_platforms:
            adapter = self._registry.get(platform)
            if not adapter:
                pending = True
                notes_parts.append(f"{platform.value}: adapter not implemented yet.")
                platform_results[platform.value] = {
                    "status": "pending",
                    "reference_id": None,
                    "message": "Adapter not implemented yet.",
                }
                continue

            description = (
                (platform_variants or {}).get(platform.value) or master_description
            )
            result = await adapter.publish(
                listing_id=listing_id,
                request=request,
                description=description,
                recommended_price=recommended_price,
                enhanced_assets=enhanced_assets,
            )
            platform_results[platform.value] = {
                "status": result.status,
                "reference_id": result.reference_id,
                "message": result.message,
                "data": result.data or {},
            }

            if result.status == "live":
                confirmed.append(platform)
            elif result.status == "failed":
                failed.append(platform)
                notes_parts.append(f"{platform.value}: {result.message}")
            else:
                pending = True
                notes_parts.append(
                    f"{platform.value}: awaiting confirmation ({result.message})"
                )

        if not notes_parts:
            notes_parts.append("All requested platforms confirmed.")

        return PublishResult(
            pending=pending,
            confirmed_platforms=confirmed,
            failed_platforms=failed,
            notes=" ".join(notes_parts),
            platform_results=platform_results,
        )
