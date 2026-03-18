import time
import uuid

from .pipelines.description_generator import DescriptionGenerator
from .pipelines.image_enhancer import ImageEnhancer
from .pipelines.publisher import ChannelPublisher, PublishResult
from .compliance import ComplianceReviewer
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
        reviewer: ComplianceReviewer | None = None,
        perception: PerceptionEngine | None = None,
        storage: ListingStore | None = None,
        telemetry: TelemetryClient | None = None,
    ) -> None:
        self._enhancer = enhancer
        self._copywriter = copywriter
        self._publisher = publisher
        self._reviewer = reviewer or ComplianceReviewer()
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

        compliance_review = self._reviewer.review_listing(payload)
        self._record(
            "listing.compliance_checked",
            listing_id,
            {
                "status": compliance_review.status,
                "reason_count": len(compliance_review.reasons),
            },
        )
        if compliance_review.status == "blocked":
            response = schemas.ListingResponse(
                status=schemas.ListingStatus(
                    listing_id=listing_id,
                    state="blocked",
                    platforms_live=[],
                    notes="Request blocked by compliance policy.",
                ),
                compliance_review=compliance_review,
                recommended_price=None,
                title_options=[],
                selected_title=None,
                preview_description=None,
                platform_variants={},
                platform_publication={},
                verified_attributes={},
                perception_report={},
                quality_report={},
                enhanced_assets=[],
            )
            self._record(
                "listing.blocked",
                listing_id,
                {
                    "duration_ms": round((time.perf_counter() - overall_start) * 1000, 2),
                    "reasons": compliance_review.reasons,
                },
            )
            self._persist_listing(listing_id, payload, response)
            return response

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
        publish_requested = publish and bool(payload.target_platforms)
        publish_allowed = publish_requested and compliance_review.status == "passed"
        if publish_requested and not publish_allowed:
            self._record(
                "listing.publication_skipped",
                listing_id,
                {"compliance_status": compliance_review.status},
            )
        if publish_allowed:
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
        elif publish_requested and compliance_review.status == "needs_review":
            status = schemas.ListingStatus(
                listing_id=listing_id,
                state="needs_review",
                platforms_live=[],
                notes="Draft generated; manual compliance review required before publishing.",
            )
            platform_publication = {}
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
            compliance_review=compliance_review,
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

        self._persist_listing(listing_id, payload, response)

        return response

    def _record(self, event: str, listing_id: str, payload: dict | None = None) -> None:
        try:
            self._telemetry.record_event(event, listing_id, payload)
        except Exception:
            # Telemetry should never block main workflow; swallow errors silently for now.
            pass

    def _persist_listing(
        self,
        listing_id: str,
        payload: schemas.ListingRequest,
        response: schemas.ListingResponse,
    ) -> None:
        # Persistence should not block listing creation.
        try:
            req_dump = payload.model_dump(mode="json")
            res_dump = response.model_dump(mode="json")
            self._storage.upsert_listing(
                listing_id=listing_id,
                owner_id=payload.owner_id,
                request=req_dump,
                response=res_dump,
            )
            if response.platform_publication:
                self._storage.create_publish_jobs(
                    listing_id=listing_id,
                    platform_publication=response.platform_publication,
                    mode_by_platform={
                        k: "assisted" for k in response.platform_publication.keys()
                    },
                )
        except Exception:
            pass
