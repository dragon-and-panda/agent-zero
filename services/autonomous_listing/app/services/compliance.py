from __future__ import annotations

import re
from typing import List

from .. import schemas
from .knowledge_base import KnowledgeBase, get_knowledge_base


class ComplianceChecker:
    """
    Lightweight heuristic validator inspired by the policy pack.
    It is not a substitute for full legal review, but it enforces high-signal guardrails.
    """

    _PHONE_REGEX = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
    _BANNED_PHRASES = ("cash only", "wire transfer", "off-platform", "venmo me")

    def __init__(self, knowledge_base: KnowledgeBase | None = None) -> None:
        self._knowledge = knowledge_base or get_knowledge_base()

    def evaluate(
        self, request: schemas.ListingRequest, description: str
    ) -> List[schemas.ComplianceFinding]:
        findings: List[schemas.ComplianceFinding] = []
        lowered = description.lower()

        if self._PHONE_REGEX.search(description):
            findings.append(
                schemas.ComplianceFinding(
                    rule="Craigslist contact policy",
                    severity="error",
                    message="Detected phone number in description. Use marketplace relay channels.",
                )
            )

        for phrase in self._BANNED_PHRASES:
            if phrase in lowered:
                findings.append(
                    schemas.ComplianceFinding(
                        rule="Marketplace prohibited phrasing",
                        severity="error",
                        message=f"Detected banned phrase '{phrase}'. Remove off-platform payment instructions.",
                    )
                )

        if request.preferences.pickup_only and "pickup" not in lowered:
            findings.append(
                schemas.ComplianceFinding(
                    rule="Pickup disclosure",
                    severity="warning",
                    message="Seller requested pickup-only but description lacks pickup instructions.",
                )
            )

        if request.target_platforms:
            if schemas.PlatformEnum.mercari in request.target_platforms:
                if "condition" not in lowered:
                    findings.append(
                        schemas.ComplianceFinding(
                            rule="Mercari condition tag",
                            severity="warning",
                            message="Mention item condition explicitly to satisfy Mercari requirements.",
                        )
                    )

        if request.target_platforms and schemas.PlatformEnum.nextdoor in request.target_platforms:
            if "neighborhood" not in lowered and "community" not in lowered:
                findings.append(
                    schemas.ComplianceFinding(
                        rule="Nextdoor community context",
                        severity="info",
                        message="Consider referencing the local neighborhood to boost trust.",
                    )
                )

        return findings
