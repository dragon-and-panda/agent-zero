import unittest

from app import schemas
from app.services.compliance import ComplianceReviewer
from app.services.orchestrator import ListingOrchestrator, PublishResult
from app.services.pipelines.description_generator import CopyPackage


class DummyEnhancer:
    async def process(self, listing_id, assets):
        return ["https://example.com/enhanced.jpg"]


class DummyCopywriter:
    async def generate(self, listing_id, request, enhanced_assets, verified_attributes=None):
        return CopyPackage(
            master_description="Clean and accurate listing copy.",
            suggested_price=42.0,
            platform_variants={},
            quality_report={"score": 91},
            title_options=["Walnut Coffee Table"],
            selected_title="Walnut Coffee Table",
        )


class DummyPublisher:
    def __init__(self):
        self.calls = 0

    async def schedule_publication(
        self,
        listing_id,
        request,
        enhanced_assets,
        master_description,
        platform_variants,
        recommended_price,
    ):
        self.calls += 1
        return PublishResult(
            pending=False,
            confirmed_platforms=[schemas.PlatformEnum.craigslist],
            notes="Published.",
            platform_results={
                "craigslist": {
                    "status": "live",
                    "reference_id": "abc123",
                    "message": "Published.",
                    "data": {},
                }
            },
        )


class DummyPerception:
    async def infer_verified_attributes(self, request):
        return {"material": "walnut"}, {"confidence": "high"}


class DummyStorage:
    def upsert_listing(self, listing_id, owner_id, request, response):
        return None

    def create_publish_jobs(self, listing_id, platform_publication, mode_by_platform):
        return None


class DummyTelemetry:
    def record_event(self, event, listing_id, payload):
        return None


class ComplianceReviewerTests(unittest.TestCase):
    def test_blocks_personal_contact_data_brokerage(self):
        reviewer = ComplianceReviewer()
        request = schemas.ListingRequest(
            raw_description="Huge email list from scraped contacts and inbox exports.",
            category="marketing",
        )

        review = reviewer.review_listing(request)

        self.assertEqual(review.status, "blocked")
        self.assertTrue(
            any("Personal contact data" in reason for reason in review.reasons)
        )


class OrchestratorComplianceTests(unittest.IsolatedAsyncioTestCase):
    def _build_orchestrator(self, publisher):
        return ListingOrchestrator(
            enhancer=DummyEnhancer(),
            copywriter=DummyCopywriter(),
            publisher=publisher,
            perception=DummyPerception(),
            storage=DummyStorage(),
            telemetry=DummyTelemetry(),
        )

    async def test_publish_is_skipped_without_attestations(self):
        publisher = DummyPublisher()
        orchestrator = self._build_orchestrator(publisher)
        request = schemas.ListingRequest(
            raw_description="Mid-century walnut coffee table with minor wear.",
            category="furniture",
            location="Austin, TX",
            target_platforms=[schemas.PlatformEnum.craigslist],
        )

        response = await orchestrator.create_listing(request, publish=True)

        self.assertEqual(response.compliance_review.status, "needs_review")
        self.assertEqual(response.status.state, "needs_review")
        self.assertEqual(publisher.calls, 0)

    async def test_publish_runs_after_attestations(self):
        publisher = DummyPublisher()
        orchestrator = self._build_orchestrator(publisher)
        request = schemas.ListingRequest(
            raw_description="Mid-century walnut coffee table with minor wear.",
            category="furniture",
            location="Austin, TX",
            target_platforms=[schemas.PlatformEnum.craigslist],
            seller_attestations=schemas.SellerAttestation(
                owns_or_can_sell_item=True,
                description_is_truthful=True,
                no_prohibited_items=True,
            ),
        )

        response = await orchestrator.create_listing(request, publish=True)

        self.assertEqual(response.compliance_review.status, "passed")
        self.assertEqual(response.status.state, "live")
        self.assertEqual(publisher.calls, 1)


if __name__ == "__main__":
    unittest.main()
