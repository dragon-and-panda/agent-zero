from dataclasses import dataclass

from python.helpers.tool import Response, Tool

VALID_LEVELS = {"low", "medium", "high"}
PROHIBITED_PATTERNS = {
    "sell email list": "selling personal email lists is prohibited",
    "broker email list": "brokering personal contact lists is prohibited",
    "harvest emails": "harvesting personal emails is prohibited",
    "scrape gmail": "scraping Gmail data for resale is prohibited",
    "gmail scraping": "scraping Gmail data for resale is prohibited",
    "compile email addresses": "compiling personal email lists for resale is prohibited",
    "contact list resale": "reselling contact lists is prohibited",
    "non-consensual outreach": "non-consensual outreach is prohibited",
    "cold spam": "spam-based acquisition is prohibited",
}


@dataclass
class RevenuePlan:
    venture: str
    customer: str
    acquisition: str
    fulfillment: str
    notes: str
    legality: str
    consent: str
    provenance: str
    platform_risk: str
    time: str
    margin: str
    repeatability: str
    automation: str
    defensibility: str


class RevenuePlanning(Tool):
    async def execute(
        self,
        venture: str = "",
        customer: str = "",
        acquisition: str = "",
        fulfillment: str = "",
        notes: str = "",
        legality: str = "medium",
        consent: str = "medium",
        provenance: str = "medium",
        platform_risk: str = "medium",
        time: str = "medium",
        margin: str = "medium",
        repeatability: str = "medium",
        automation: str = "medium",
        defensibility: str = "medium",
        **kwargs,
    ):
        try:
            plan = RevenuePlan(
                venture=venture.strip(),
                customer=customer.strip(),
                acquisition=acquisition.strip(),
                fulfillment=fulfillment.strip(),
                notes=notes.strip(),
                legality=normalize_level("legality", legality),
                consent=normalize_level("consent", consent),
                provenance=normalize_level("provenance", provenance),
                platform_risk=normalize_level("platform_risk", platform_risk),
                time=normalize_level("time", time),
                margin=normalize_level("margin", margin),
                repeatability=normalize_level("repeatability", repeatability),
                automation=normalize_level("automation", automation),
                defensibility=normalize_level("defensibility", defensibility),
            )
        except ValueError as exc:
            return Response(message=f"Revenue planning input error: {exc}", break_loop=False)

        result = evaluate_plan(plan)
        return Response(message=format_result(plan, result), break_loop=False)


def normalize_level(name: str, value: str) -> str:
    normalized = (value or "medium").strip().lower()
    if normalized not in VALID_LEVELS:
        raise ValueError(f"{name} must be one of: low, medium, high")
    return normalized


def evaluate_plan(plan: RevenuePlan) -> dict:
    findings: list[str] = []
    next_steps: list[str] = []

    prohibited_hits = detect_prohibited_patterns(plan)
    if prohibited_hits:
        findings.extend(prohibited_hits)
        next_steps.extend(
            [
                "Replace personal-data resale with opt-in lead capture or a client-owned workflow.",
                "Keep inbox and contact data inside the owner's CRM or support workflow.",
                "Re-score the revised lane only after consent and provenance are explicit.",
            ]
        )
        return {
            "verdict": "REJECT",
            "findings": findings,
            "next_steps": next_steps,
        }

    if plan.legality == "low":
        findings.append("Legal confidence is too low.")
    if plan.consent == "low":
        findings.append("Consent is missing or too weak.")
    if plan.provenance == "low":
        findings.append("Data provenance is unclear or unsafe.")
    if plan.platform_risk == "high":
        findings.append("Platform or terms-of-service risk is too high.")

    if findings:
        next_steps.extend(
            [
                "Redesign the offer so it does not depend on prohibited data or high-risk platform behavior.",
                "Document the lawful data source and the customer authorization path.",
                "Do not launch until the hard-gate issues are resolved.",
            ]
        )
        return {
            "verdict": "REJECT",
            "findings": findings,
            "next_steps": next_steps,
        }

    if plan.legality == "medium":
        findings.append("Legality needs stronger evidence before launch.")
    if plan.consent == "medium":
        findings.append("Consent mechanics need to be tightened before launch.")
    if plan.provenance == "medium":
        findings.append("Data provenance needs stronger documentation before launch.")
    if plan.platform_risk == "medium":
        findings.append("Platform risk needs mitigation before launch.")

    soft_factors = {
        "time": plan.time,
        "margin": plan.margin,
        "repeatability": plan.repeatability,
        "automation": plan.automation,
        "defensibility": plan.defensibility,
    }
    soft_high_count = sum(1 for value in soft_factors.values() if value == "high")
    soft_low = [name for name, value in soft_factors.items() if value == "low"]

    for name in soft_low:
        findings.append(f"{pretty_name(name)} is too weak.")

    if not findings and soft_high_count >= 3:
        next_steps.extend(
            [
                "Draft the offer, price point, and first acquisition experiment.",
                "Define activation metrics and ongoing compliance checks.",
                "Keep the launch narrow until the first customer proof appears.",
            ]
        )
        return {
            "verdict": "PASS",
            "findings": ["Hard gates are clear and execution factors are attractive."],
            "next_steps": next_steps,
        }

    if not findings:
        findings.append("The lane is compliant but not yet strong enough to activate.")

    next_steps.extend(
        [
            "Strengthen the weak execution factors before launch.",
            "Tighten the customer offer, acquisition motion, or delivery model.",
            "Re-score after the revised operating plan is documented.",
        ]
    )
    return {
        "verdict": "HOLD",
        "findings": findings,
        "next_steps": next_steps,
    }


def detect_prohibited_patterns(plan: RevenuePlan) -> list[str]:
    searchable_text = " ".join(
        [
            plan.venture,
            plan.customer,
            plan.acquisition,
            plan.fulfillment,
            plan.notes,
        ]
    ).lower()
    hits: list[str] = []
    for pattern, reason in PROHIBITED_PATTERNS.items():
        if pattern in searchable_text:
            hits.append(reason)
    return hits


def pretty_name(name: str) -> str:
    return name.replace("_", " ")


def format_result(plan: RevenuePlan, result: dict) -> str:
    hard_factors = {
        "legality": plan.legality,
        "consent": plan.consent,
        "provenance": plan.provenance,
        "platform risk": plan.platform_risk,
    }
    soft_factors = {
        "time": plan.time,
        "margin": plan.margin,
        "repeatability": plan.repeatability,
        "automation": plan.automation,
        "defensibility": plan.defensibility,
    }

    lines = [
        f"Revenue lane: {plan.venture or 'Untitled lane'}",
        f"Verdict: {result['verdict']}",
        "",
        "Business model",
        f"- Customer: {plan.customer or 'unspecified'}",
        f"- Acquisition: {plan.acquisition or 'unspecified'}",
        f"- Fulfillment: {plan.fulfillment or 'unspecified'}",
    ]

    if plan.notes:
        lines.append(f"- Notes: {plan.notes}")

    lines.extend(["", "Hard gates"])
    for key, value in hard_factors.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "Execution factors"])
    for key, value in soft_factors.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "Findings"])
    for finding in result["findings"]:
        lines.append(f"- {finding}")

    lines.extend(["", "Recommended next steps"])
    for step in result["next_steps"]:
        lines.append(f"- {step}")

    return "\n".join(lines)
