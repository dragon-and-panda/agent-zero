from python.helpers.tool import Tool, Response


SOFT_FACTORS = (
    "time_to_cash",
    "margin",
    "repeatability",
    "automation_fit",
    "defensibility",
)

ALLOWED_LEVELS = {"low", "medium", "high"}


class RevenuePlanning(Tool):

    async def execute(
        self,
        venture="",
        customer="",
        offer="",
        acquisition_channel="",
        fulfillment="",
        legality="",
        consent="",
        data_provenance="",
        platform_terms="",
        time_to_cash="",
        margin="",
        repeatability="",
        automation_fit="",
        defensibility="",
        notes="",
        **kwargs,
    ):
        hard_gates = {
            "legality": legality,
            "consent": consent,
            "data_provenance": data_provenance,
            "platform_terms": platform_terms,
        }
        normalized_hard_gates = {
            name: normalize_level(value) for name, value in hard_gates.items()
        }
        soft_factors = {
            "time_to_cash": time_to_cash,
            "margin": margin,
            "repeatability": repeatability,
            "automation_fit": automation_fit,
            "defensibility": defensibility,
        }
        normalized_soft_factors = {
            name: normalize_level(value) for name, value in soft_factors.items()
        }

        problems = collect_invalid_inputs(normalized_hard_gates | normalized_soft_factors)
        if problems:
            message = (
                "Revenue plan input invalid.\n"
                + "\n".join(f"- {problem}" for problem in problems)
                + "\nUse only low, medium, or high for gating fields."
            )
            return Response(message=message, break_loop=False)

        decision, decision_reasons = classify_plan(
            normalized_hard_gates, normalized_soft_factors
        )
        summary = format_summary(
            venture=venture,
            customer=customer,
            offer=offer,
            acquisition_channel=acquisition_channel,
            fulfillment=fulfillment,
            hard_gates=normalized_hard_gates,
            soft_factors=normalized_soft_factors,
            notes=notes,
            decision=decision,
            decision_reasons=decision_reasons,
        )
        return Response(message=summary, break_loop=False)


def normalize_level(value: str) -> str:
    return str(value).strip().lower()


def collect_invalid_inputs(inputs: dict[str, str]) -> list[str]:
    problems: list[str] = []
    for field, value in inputs.items():
        if value not in ALLOWED_LEVELS:
            problems.append(f"{field}={value!r}")
    return problems


def classify_plan(
    hard_gates: dict[str, str], soft_factors: dict[str, str]
) -> tuple[str, list[str]]:
    low_hard_gates = [name for name, value in hard_gates.items() if value == "low"]
    if low_hard_gates:
        return (
            "REJECT",
            [
                "Hard gate failed: "
                + ", ".join(low_hard_gates)
                + ". Do not execute this venture lane."
            ],
        )

    medium_hard_gates = [name for name, value in hard_gates.items() if value == "medium"]
    low_soft_factors = [name for name, value in soft_factors.items() if value == "low"]
    medium_soft_factors = [
        name for name, value in soft_factors.items() if value == "medium"
    ]

    reasons: list[str] = []
    if medium_hard_gates:
        reasons.append(
            "Hard gates need stronger proof before launch: " + ", ".join(medium_hard_gates)
        )
    if low_soft_factors:
        reasons.append(
            "Commercial fundamentals are weak: " + ", ".join(low_soft_factors)
        )
    if medium_soft_factors:
        reasons.append(
            "Commercial fundamentals are promising but still need validation: "
            + ", ".join(medium_soft_factors)
        )

    if reasons:
        return ("HOLD", reasons)

    return (
        "PASS",
        [
            "All hard gates cleared and all commercial fundamentals are high.",
            "Lane can move into a controlled pilot with monitoring."
        ],
    )


def format_summary(
    *,
    venture: str,
    customer: str,
    offer: str,
    acquisition_channel: str,
    fulfillment: str,
    hard_gates: dict[str, str],
    soft_factors: dict[str, str],
    notes: str,
    decision: str,
    decision_reasons: list[str],
) -> str:
    lines = [
        f"Decision: {decision}",
        "",
        "Venture summary:",
        f"- Venture: {venture or 'unspecified'}",
        f"- Customer: {customer or 'unspecified'}",
        f"- Offer: {offer or 'unspecified'}",
        f"- Acquisition channel: {acquisition_channel or 'unspecified'}",
        f"- Fulfillment: {fulfillment or 'unspecified'}",
        "",
        "Hard gates:",
    ]
    for name, value in hard_gates.items():
        lines.append(f"- {pretty_name(name)}: {value}")

    lines.append("")
    lines.append("Commercial fundamentals:")
    for name in SOFT_FACTORS:
        lines.append(f"- {pretty_name(name)}: {soft_factors[name]}")

    lines.append("")
    lines.append("Why:")
    for reason in decision_reasons:
        lines.append(f"- {reason}")

    next_steps = next_step_guidance(decision, hard_gates, soft_factors)
    lines.append("")
    lines.append("Next steps:")
    for step in next_steps:
        lines.append(f"- {step}")

    if notes.strip():
        lines.append("")
        lines.append("Notes:")
        lines.append(notes.strip())

    return "\n".join(lines)


def next_step_guidance(
    decision: str, hard_gates: dict[str, str], soft_factors: dict[str, str]
) -> list[str]:
    if decision == "REJECT":
        return [
            "Replace any personal-data, scraping, or resale mechanism with first-party or explicit opt-in acquisition.",
            "Re-scope the offer around lawful deliverables such as research, services, software, or client-owned CRM workflows.",
            "Do not automate execution until all hard gates are at least medium."
        ]

    if decision == "HOLD":
        steps: list[str] = []
        medium_hard_gates = [name for name, value in hard_gates.items() if value == "medium"]
        low_soft_factors = [name for name, value in soft_factors.items() if value == "low"]
        medium_soft_factors = [
            name for name, value in soft_factors.items() if value == "medium"
        ]
        if medium_hard_gates:
            steps.append(
                "Gather concrete proof for: " + ", ".join(pretty_name(name) for name in medium_hard_gates) + "."
            )
        if low_soft_factors:
            steps.append(
                "Improve or replace weak fundamentals: "
                + ", ".join(pretty_name(name) for name in low_soft_factors)
                + "."
            )
        if medium_soft_factors:
            steps.append(
                "Run a small validation sprint for: "
                + ", ".join(pretty_name(name) for name in medium_soft_factors)
                + "."
            )
        steps.append("Keep execution in research or pilot mode until the lane scores PASS.")
        return steps

    return [
        "Launch a controlled pilot with first-party analytics and explicit consent records.",
        "Track conversion, margin, time-to-cash, and fulfillment load before scaling.",
        "Document outcomes in docs/programs/agentic_financial_system/journal.md."
    ]


def pretty_name(name: str) -> str:
    return name.replace("_", " ")
