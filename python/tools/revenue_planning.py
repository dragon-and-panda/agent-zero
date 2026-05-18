from python.helpers.tool import Tool, Response


CLEAR_GATE_VALUES = {
    "yes",
    "clear",
    "compliant",
    "allowed",
    "owner-authorized",
    "owner-controlled",
    "client-owned",
    "contracted",
}
FAIL_GATE_VALUES = {
    "no",
    "fail",
    "failed",
    "blocked",
    "illegal",
    "non-compliant",
    "noncompliant",
    "unclear",
    "unknown",
    "unsure",
    "",
}
CLEAR_PROVENANCE_VALUES = {
    "first-party",
    "client-owned",
    "owner-authorized",
    "public-business",
    "public-nonpersonal",
    "synthetic",
}
HIGH_VALUES = {"high", "strong", "fast", "good"}
MEDIUM_VALUES = {"medium", "moderate", "mixed", "ok"}
LOW_VALUES = {"low", "weak", "slow", "poor"}
UNSAFE_PATTERNS = {
    "personal-data resale": (
        "sell email list",
        "sell email lists",
        "sell contact list",
        "sell contact lists",
        "broker email list",
        "broker contact list",
        "rent email list",
        "resell contacts",
    ),
    "non-consensual inbox mining": (
        "scrape gmail",
        "mine gmail",
        "extract emails from gmail",
        "harvest emails from gmail",
        "compile email list from gmail",
        "pull contacts from inbox",
    ),
    "spam-first acquisition": (
        "mass cold email",
        "bulk unsolicited outreach",
        "scrape leads for outreach",
        "blast outreach",
    ),
}


def _normalize_text(value: str) -> str:
    return str(value).strip().lower()


def _normalize_gate(value: str) -> str:
    normalized = _normalize_text(value)
    if normalized in CLEAR_GATE_VALUES:
        return "yes"
    if normalized in FAIL_GATE_VALUES:
        return "no"
    return normalized or "no"


def _normalize_provenance(value: str) -> str:
    normalized = _normalize_text(value)
    if normalized in CLEAR_PROVENANCE_VALUES:
        return normalized
    return normalized or "unclear"


def _normalize_soft_factor(value: str) -> str:
    normalized = _normalize_text(value)
    if normalized in HIGH_VALUES:
        return "high"
    if normalized in LOW_VALUES:
        return "low"
    if normalized in MEDIUM_VALUES:
        return "medium"
    return "medium"


def _detect_unsafe_patterns(*values: str) -> list[str]:
    haystack = " ".join(_normalize_text(value) for value in values if value)
    matches: list[str] = []
    for label, patterns in UNSAFE_PATTERNS.items():
        if any(pattern in haystack for pattern in patterns):
            matches.append(label)
    return matches


def _format_mapping(title: str, values: dict[str, str]) -> str:
    lines = [title]
    for key, value in values.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


class RevenuePlanning(Tool):
    async def execute(
        self,
        opportunity: str = "",
        customer: str = "",
        offer: str = "",
        acquisition: str = "",
        data_provenance: str = "",
        consent_model: str = "",
        legal: str = "",
        platform_terms: str = "",
        delivery: str = "",
        time_to_cash: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation_fit: str = "medium",
        defensibility: str = "medium",
        **kwargs,
    ):
        hard_gates = {
            "legal": _normalize_gate(legal),
            "consent": _normalize_gate(consent_model),
            "provenance": _normalize_provenance(data_provenance),
            "platform_terms": _normalize_gate(platform_terms),
            "delivery": _normalize_gate(delivery),
        }
        soft_factors = {
            "time_to_cash": _normalize_soft_factor(time_to_cash),
            "margin": _normalize_soft_factor(margin),
            "repeatability": _normalize_soft_factor(repeatability),
            "automation_fit": _normalize_soft_factor(automation_fit),
            "defensibility": _normalize_soft_factor(defensibility),
        }
        unsafe_flags = _detect_unsafe_patterns(
            opportunity,
            offer,
            acquisition,
            data_provenance,
        )

        hard_failures: list[str] = []
        if hard_gates["legal"] != "yes":
            hard_failures.append("legal")
        if hard_gates["consent"] != "yes":
            hard_failures.append("consent")
        if hard_gates["provenance"] not in CLEAR_PROVENANCE_VALUES:
            hard_failures.append("provenance")
        if hard_gates["platform_terms"] != "yes":
            hard_failures.append("platform_terms")
        if hard_gates["delivery"] != "yes":
            hard_failures.append("delivery")
        if unsafe_flags:
            hard_failures.extend(unsafe_flags)

        high_count = sum(1 for value in soft_factors.values() if value == "high")
        low_soft = [label for label, value in soft_factors.items() if value == "low"]

        decision = "HOLD"
        rationale = "Hard gates clear, but the lane is not attractive enough yet."
        recommendations = [
            "Tighten the offer, ICP, and pricing until at least three soft factors are high.",
            "Keep the lane parked until the weak execution factors are improved.",
        ]

        if hard_failures:
            decision = "REJECT"
            rationale = "This lane fails required compliance or feasibility gates."
            recommendations = [
                "Replace personal-data resale or ambiguous-data ideas with first-party or client-owned services.",
                "Require explicit owner authorization, documented provenance, and a terms-compliant delivery path.",
                "Redirect toward opt-in lead capture, research products, listing services, or workflow automation retainers.",
            ]
        elif not low_soft and high_count >= 3:
            decision = "PASS"
            rationale = "Hard gates clear, no soft factor is low, and at least three soft factors are high."
            recommendations = [
                "Run a narrow pilot with one ICP, one acquisition channel, and one delivery SOP.",
                "Track time to first value, margin, and repeatability before expanding the lane.",
            ]

        overview = {
            "opportunity": opportunity or "not provided",
            "customer": customer or "not provided",
            "offer": offer or "not provided",
            "acquisition": acquisition or "not provided",
        }
        lines = [
            f"Decision: {decision}",
            f"Rationale: {rationale}",
            "",
            _format_mapping("Overview", overview),
            "",
            _format_mapping("Hard gates", hard_gates),
            "",
            _format_mapping("Soft factors", soft_factors),
            "",
            f"High soft-factor count: {high_count}",
            f"Low soft factors: {', '.join(low_soft) if low_soft else 'none'}",
            f"Unsafe flags: {', '.join(unsafe_flags) if unsafe_flags else 'none'}",
            "",
            "Recommended next steps",
        ]
        for index, recommendation in enumerate(recommendations, start=1):
            lines.append(f"{index}. {recommendation}")

        return Response(message="\n".join(lines), break_loop=False)
