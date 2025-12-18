import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List

from .pipelines.description_generator import DescriptionGenerator
from .pipelines.image_enhancer import ImageEnhancer
from .pipelines.publisher import ChannelPublisher
from .perception import PerceptionEngine
from .storage import ListingStore
from .telemetry import TelemetryClient
from .. import schemas


class ListingOrchestrator:
    """Thin coordination layer that chains the enhancement, copywriting, pricing and publishing steps."""

    def __init__(
        self,
        enhancer: ImageEnhancer,
        copywriter: DescriptionGenerator,
        publisher: ChannelPublisher,
        perception: PerceptionEngine | None = None,
        storage: ListingStore | None = None,
        telemetry: TelemetryClient | None = None,
    ) -> None:
        self._enhancer = enhancer
        self._copywriter = copywriter
        self._publisher = publisher
        self._perception = perception or PerceptionEngine()
        self._storage = storage or ListingStore()
        self._telemetry = telemetry or TelemetryClient()

    async def create_listing(
        self, payload: schemas.ListingRequest, publish: bool = True
    ) -> schemas.ListingResponse:
        listing_id = str(uuid.uuid4())
        overall_start = time.perf_counter()

        self._record(
            "listing.request_received",
            listing_id,
            {
                "category": payload.category,
                "platforms_requested": [p.value for p in payload.target_platforms],
                "asset_count": len(payload.assets),
            },
        )

        stage_start = time.perf_counter()
        enhanced_assets = await self._enhancer.process(listing_id, payload.assets)
        self._record(
            "listing.images_enhanced",
            listing_id,
            {
                "asset_count": len(enhanced_assets),
                "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
            },
        )

        stage_start = time.perf_counter()
        verified_attributes, perception_report = await self._perception.infer_verified_attributes(
            request=payload
        )
        self._record(
            "listing.perception_complete",
            listing_id,
            {
                "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                "verified_keys": list(verified_attributes.keys()),
            },
        )

        stage_start = time.perf_counter()
        copy_pkg = await self._copywriter.generate(
            listing_id=listing_id,
            request=payload,
            enhanced_assets=enhanced_assets,
            verified_attributes=verified_attributes,
        )
        preview_description = copy_pkg.master_description
        suggested_price = copy_pkg.suggested_price
        self._record(
            "listing.copy_generated",
            listing_id,
            {
                "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                "suggested_price": suggested_price,
                "quality_score": copy_pkg.quality_report.get("score")
                if isinstance(copy_pkg.quality_report, dict)
                else None,
            },
        )

        publish_results = None
        if publish and payload.target_platforms:
            stage_start = time.perf_counter()
            publish_results = await self._publisher.schedule_publication(
                listing_id=listing_id,
                request=payload,
                enhanced_assets=enhanced_assets,
                master_description=preview_description,
                platform_variants=copy_pkg.platform_variants,
                recommended_price=suggested_price,
            )
            self._record(
                "listing.publication_triggered",
                listing_id,
                {
                    "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                    "pending": publish_results.pending,
                    "confirmed_platforms": [
                        p.value for p in publish_results.confirmed_platforms
                    ],
                },
            )

        if publish_results:
            status = schemas.ListingStatus(
                listing_id=listing_id,
                state="publishing" if publish_results.pending else "live",
                platforms_live=publish_results.confirmed_platforms,
                notes=publish_results.notes,
            )
            platform_publication = publish_results.platform_results
        else:
            status = schemas.ListingStatus(
                listing_id=listing_id,
                state="drafted",
                platforms_live=[],
                notes="Draft generated; not published.",
            )
            platform_publication = {}

        response = schemas.ListingResponse(
            status=status,
            recommended_price=suggested_price,
            title_options=copy_pkg.title_options,
            selected_title=copy_pkg.selected_title,
            preview_description=preview_description,
            platform_variants=copy_pkg.platform_variants,
            platform_publication=platform_publication,
            verified_attributes=verified_attributes,
            perception_report=perception_report,
            quality_report=copy_pkg.quality_report,
            enhanced_assets=enhanced_assets,
        )

        self._record(
            "listing.response_ready",
            listing_id,
            {
                "state": status.state,
                "duration_ms": round((time.perf_counter() - overall_start) * 1000, 2),
            },
        )

        # Persist listing + create publish jobs (assisted by default).
        try:
            req_dump = payload.model_dump(mode="json")
            res_dump = response.model_dump(mode="json")
            owner_id = payload.owner_id
            self._storage.upsert_listing(
                listing_id=listing_id,
                owner_id=owner_id,
                request=req_dump,
                response=res_dump,
            )
            if platform_publication:
                self._storage.create_publish_jobs(
                    listing_id=listing_id,
                    platform_publication=platform_publication,
                    mode_by_platform={k: "assisted" for k in platform_publication.keys()},
                )
        except Exception:
            # Persistence should not block listing creation.
            pass

        return response

    def _record(self, event: str, listing_id: str, payload: dict | None = None) -> None:
        try:
            self._telemetry.record_event(event, listing_id, payload)
        except Exception:
            # Telemetry should never block main workflow; swallow errors silently for now.
            pass


@dataclass
class PublishResult:
    pending: bool
    confirmed_platforms: List[schemas.PlatformEnum] = field(default_factory=list)
    failed_platforms: List[schemas.PlatformEnum] = field(default_factory=list)
    notes: str = ""
    platform_results: Dict[str, dict] = field(default_factory=dict)
