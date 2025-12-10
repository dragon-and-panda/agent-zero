import time
import uuid
from dataclasses import dataclass, field
from typing import List

from .compliance import ComplianceChecker
from .pipelines.description_generator import DescriptionGenerator
from .pipelines.image_enhancer import ImageEnhancer
from .pipelines.publisher import ChannelPublisher
from .telemetry import TelemetryClient
from .. import schemas


class ListingOrchestrator:
    """Thin coordination layer that chains the enhancement, copywriting, pricing and publishing steps."""

    def __init__(
        self,
        enhancer: ImageEnhancer,
        copywriter: DescriptionGenerator,
        publisher: ChannelPublisher,
        telemetry: TelemetryClient | None = None,
        compliance: ComplianceChecker | None = None,
    ) -> None:
        self._enhancer = enhancer
        self._copywriter = copywriter
        self._publisher = publisher
        self._telemetry = telemetry or TelemetryClient()
        self._compliance = compliance or ComplianceChecker()

    async def create_listing(
        self, payload: schemas.ListingRequest
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
        preview_description, suggested_price = await self._copywriter.generate(
            listing_id=listing_id,
            request=payload,
            enhanced_assets=enhanced_assets,
        )
        self._record(
            "listing.copy_generated",
            listing_id,
            {
                "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                "suggested_price": suggested_price,
            },
        )

        compliance_findings = self._compliance.evaluate(payload, preview_description)
        compliance_report = self._build_compliance_report(compliance_findings)
        self._record(
            "listing.compliance_checked",
            listing_id,
            {
                "issues": len(compliance_findings),
                "blocking": not compliance_report.passed,
            },
        )

        stage_start = time.perf_counter()
        publish_results = await self._publisher.schedule_publication(
            listing_id=listing_id,
            request=payload,
            enhanced_assets=enhanced_assets,
            description=preview_description,
            recommended_price=suggested_price,
        )
        self._record(
            "listing.publication_triggered",
            listing_id,
            {
                "duration_ms": round((time.perf_counter() - stage_start) * 1000, 2),
                "pending": publish_results.pending,
                "confirmed_platforms": [p.value for p in publish_results.confirmed_platforms],
            },
        )

        status = schemas.ListingStatus(
            listing_id=listing_id,
            state="publishing" if publish_results.pending else "live",
            platforms_live=publish_results.confirmed_platforms,
            notes=self._compose_notes(
                publish_results.notes, compliance_report.passed
            ),
        )

        response = schemas.ListingResponse(
            status=status,
            recommended_price=suggested_price,
            preview_description=preview_description,
            enhanced_assets=enhanced_assets,
            compliance=compliance_report,
        )

        self._record(
            "listing.response_ready",
            listing_id,
            {
                "state": status.state,
                "duration_ms": round((time.perf_counter() - overall_start) * 1000, 2),
            },
        )

        return response

    def _record(self, event: str, listing_id: str, payload: dict | None = None) -> None:
        try:
            self._telemetry.record_event(event, listing_id, payload)
        except Exception:
            # Telemetry should never block main workflow; swallow errors silently for now.
            pass

    @staticmethod
    def _build_compliance_report(
        findings: List[schemas.ComplianceFinding],
    ) -> schemas.ComplianceReport:
        passed = all(f.severity != "error" for f in findings)
        return schemas.ComplianceReport(passed=passed, findings=findings)

    @staticmethod
    def _compose_notes(base_notes: str, compliance_passed: bool) -> str:
        if compliance_passed:
            return base_notes
        suffix = " Compliance review flagged issues; see report for details."
        return f"{base_notes}{suffix}"


@dataclass
class PublishResult:
    pending: bool
    confirmed_platforms: List[schemas.PlatformEnum] = field(default_factory=list)
    failed_platforms: List[schemas.PlatformEnum] = field(default_factory=list)
    notes: str = ""
