from __future__ import annotations

import re

from .. import schemas


class ComplianceReviewer:
    """Small policy gate that keeps the listing pipeline focused on lawful commerce."""

    _BLOCK_RULES = (
        (
            re.compile(
                r"\b(email list|lead list|mailing list|contact list|scraped contacts?|gmail (dump|export|inbox)|bulk email database)\b",
                re.IGNORECASE,
            ),
            "Personal contact data, scraped inbox exports, and mailing lists cannot be sold or published.",
        ),
        (
            re.compile(
                r"\b(forex signals?|managed account|guaranteed returns?|investment club|pump and dump|crypto signals?|options alerts?)\b",
                re.IGNORECASE,
            ),
            "Financial promotions, trading signals, and guaranteed-return offers are outside the scope of this service.",
        ),
    )

    _REVIEW_RULES = (
        (
            re.compile(
                r"\b(course|newsletter|membership|coaching|consulting|agency service|advisory)\b",
                re.IGNORECASE,
            ),
            "Advisory or digital offers require a manual review for platform fit and disclosure quality.",
            "Verify that the offer is accurately described and permitted on every requested platform.",
        ),
        (
            re.compile(r"\b(health claim|medical|supplement|cure|treatment)\b", re.IGNORECASE),
            "Health-adjacent claims require manual review before publishing.",
            "Remove unsupported claims and confirm the product is allowed on the target platforms.",
        ),
    )

    def review_listing(self, request: schemas.ListingRequest) -> schemas.ComplianceReview:
        corpus = self._corpus(request)
        reasons: list[str] = []
        required_actions: list[str] = []

        for pattern, message in self._BLOCK_RULES:
            if pattern.search(corpus):
                self._append_unique(reasons, message)

        if reasons:
            return schemas.ComplianceReview(
                status="blocked",
                reasons=reasons,
                required_actions=[
                    "Replace the request with a lawful product, service, or first-party offer.",
                    "Do not use this workflow for personal data brokerage or financial promotions.",
                ],
            )

        attestations = request.seller_attestations
        if not attestations.owns_or_can_sell_item:
            self._append_unique(reasons, "Seller authorization has not been attested.")
            self._append_unique(
                required_actions,
                "Confirm that you own the item or are authorized to sell it.",
            )
        if not attestations.description_is_truthful:
            self._append_unique(reasons, "Truthfulness attestation is missing.")
            self._append_unique(
                required_actions,
                "Confirm that the description, media, and claims are accurate.",
            )
        if not attestations.no_prohibited_items:
            self._append_unique(reasons, "Prohibited-item attestation is missing.")
            self._append_unique(
                required_actions,
                "Confirm that the listing does not contain prohibited or restricted goods.",
            )

        for pattern, message, action in self._REVIEW_RULES:
            if pattern.search(corpus):
                self._append_unique(reasons, message)
                self._append_unique(required_actions, action)

        if (request.delivery or "").strip().lower() == "digital":
            self._append_unique(
                reasons,
                "Digital fulfillment requires manual review before marketplace publication.",
            )
            self._append_unique(
                required_actions,
                "Confirm that the target platforms allow digital delivery for this offer.",
            )

        if reasons:
            return schemas.ComplianceReview(
                status="needs_review",
                reasons=reasons,
                required_actions=required_actions,
            )

        return schemas.ComplianceReview(
            status="passed",
            reasons=["Basic compliance checks passed."],
            required_actions=[],
        )

    def _corpus(self, request: schemas.ListingRequest) -> str:
        return " ".join(
            part
            for part in (
                request.listing_type,
                request.title_hint,
                request.raw_description,
                request.brand,
                request.condition,
                request.delivery,
                request.category,
                request.location,
            )
            if part
        )

    @staticmethod
    def _append_unique(target: list[str], value: str) -> None:
        if value not in target:
            target.append(value)
