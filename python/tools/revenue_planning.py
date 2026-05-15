import json
import re
from typing import Any

from python.helpers.tool import Response, Tool


BLOCKED_PATTERNS = {
    "email_list_brokerage": [
        r"\bemail list(s)?\b",
        r"\bsell(ing)?\s+(an?\s+)?email",
        r"\bbroker(ing)?\s+(contact|email)",
        r"\bresell(ing)?\s+(contact|email)",
        r"\bcontact list(s)?\b",
    ],
    "non_consensual_inbox_access": [
        r"\bgmail\b.{0,40}\b(extract|scrape|harvest|sell|list|broker)",
        r"\b(extract|scrape|harvest|sell|list|broker)\b.{0,40}\bgmail\b",
        r"\binbox(es)?\b.{0,40}\b(extract|scrape|harvest|sell|list|broker)",
        r"\b(extract|scrape|harvest|sell|list|broker)\b.{0,40}\binbox(es)?\b",
        r"\bmailbox(es)?\b.{0,40}\b(extract|scrape|harvest|sell|list|broker)",
        r"\b(extract|scrape|harvest|sell|list|broker)\b.{0,40}\bmailbox(es)?\b",
        r"\bharvest(ing)?\b",
    ],
    "spam_or_unsolicited_outreach": [
        r"\bmass email\b",
        r"\bcold email\b",
        r"\bunsolicited\b",
        r"\bspam\b",
        r"\bbulk outreach\b",
    ],
    "credential_or_access_abuse": [
        r"\bbypass\b",
        r"\bhack(ing)?\b",
        r"\bstolen\b",
        r"\bunauthori[sz]ed\b",
    ],
}

BLOCKED_REASON_TEXT = {
    "email_list_brokerage": "Selling or brokering personal contact lists is not an approved revenue path.",
    "non_consensual_inbox_access": "Inbox or Gmail data can only be used with explicit account-owner consent for the owner's own workflows, not for contact extraction or resale.",
    "spam_or_unsolicited_outreach": "Spam and other non-consensual outreach workflows are not allowed.",
    "credential_or_access_abuse": "Credential abuse, bypasses, or unauthorized access are not allowed.",
}

SAFE_REPLACEMENTS = [
    "Create an opt-in lead magnet and capture consented subscribers into a first-party CRM.",
    "Sell a productized service, software tool, or marketplace offering instead of personal data.",
    "Use owned documents or explicitly consented customer data for summarization, CRM hygiene, or support automation.",
    "Monetize through affiliates, digital products, or consulting tied to genuine user value.",
]


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission: str = "",
        offer: str = "",
        acquisition: str = "",
        data_handling: str = "",
        monetization: str = "",
        notes: str = "",
        **kwargs,
    ) -> Response:
        plan = evaluate_plan(
            mission=mission,
            offer=offer,
            acquisition=acquisition,
            data_handling=data_handling,
            monetization=monetization,
            notes=notes,
        )
        return Response(
            message=json.dumps(plan, indent=2, ensure_ascii=True),
            break_loop=False,
        )


def evaluate_plan(
    mission: str,
    offer: str,
    acquisition: str,
    data_handling: str,
    monetization: str,
    notes: str,
) -> dict[str, Any]:
    combined = "\n".join(
        part for part in [mission, offer, acquisition, data_handling, monetization, notes] if part
    )
    blocked_reasons = detect_blockers(combined)
    consent_status = assess_consent(acquisition, data_handling)
    provenance_status = assess_provenance(data_handling)
    platform_status = assess_platform_risk(acquisition, monetization)
    lane = suggest_lane(mission, offer, monetization)

    if blocked_reasons:
        return {
            "verdict": "REJECT",
            "policy_reference": "docs/policies/compliance_pack.md",
            "summary": "The requested monetization path fails compliance gates and should not be executed.",
            "blocked_reasons": blocked_reasons,
            "safe_replacements": SAFE_REPLACEMENTS,
        }

    open_questions = []
    if consent_status != "pass":
        open_questions.append("Clarify whether all customer or contact data is first-party and explicitly consented.")
    if provenance_status != "pass":
        open_questions.append("Document where each dataset comes from and the lawful basis for using it.")
    if platform_status != "pass":
        open_questions.append("Check the rules for the acquisition channel, marketplace, or API before automating it.")

    verdict = "PASS" if not open_questions else "HOLD"
    summary = (
        "The idea clears the initial compliance gates."
        if verdict == "PASS"
        else "The idea may be viable, but it needs compliance clarifications before execution."
    )

    return {
        "verdict": verdict,
        "policy_reference": "docs/policies/compliance_pack.md",
        "summary": summary,
        "recommended_lane": lane,
        "checks": {
            "consent": consent_status,
            "data_provenance": provenance_status,
            "platform_risk": platform_status,
        },
        "first_actions": build_first_actions(lane),
        "success_metrics": build_success_metrics(lane),
        "open_questions": open_questions,
    }


def detect_blockers(text: str) -> list[str]:
    normalized = normalize_text(text)
    reasons: list[str] = []

    for category, patterns in BLOCKED_PATTERNS.items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            reasons.append(BLOCKED_REASON_TEXT[category])

    unique_reasons: list[str] = []
    for reason in reasons:
        if reason not in unique_reasons:
            unique_reasons.append(reason)
    return unique_reasons


def assess_consent(acquisition: str, data_handling: str) -> str:
    normalized = normalize_text("\n".join([acquisition, data_handling]))
    if any(term in normalized for term in ["opt-in", "double opt-in", "consented", "customer account", "first-party"]):
        return "pass"
    if any(term in normalized for term in ["public", "scrape", "upload", "imported", "lead list"]):
        return "hold"
    return "hold" if normalized else "hold"


def assess_provenance(data_handling: str) -> str:
    normalized = normalize_text(data_handling)
    if any(term in normalized for term in ["first-party", "owned", "customer submitted", "consented", "crm"]):
        return "pass"
    if any(term in normalized for term in ["scraped", "third-party", "brokered", "unknown"]):
        return "fail"
    if any(term in normalized for term in ["gmail", "inbox", "mailbox"]):
        if any(
            term in normalized
            for term in ["own", "account owner", "summarization", "support triage", "crm hygiene"]
        ):
            return "pass"
        return "hold"
    return "hold"


def assess_platform_risk(acquisition: str, monetization: str) -> str:
    normalized = normalize_text("\n".join([acquisition, monetization]))
    risky_terms = ["scrape", "automation against terms", "bot farm", "mass dm", "bulk outreach", "shadow account"]
    if any(term in normalized for term in risky_terms):
        return "fail"
    if any(term in normalized for term in ["marketplace", "affiliate", "newsletter", "content", "saas", "service"]):
        return "pass"
    return "hold"


def suggest_lane(mission: str, offer: str, monetization: str) -> str:
    normalized = normalize_text("\n".join([mission, offer, monetization]))
    if any(term in normalized for term in ["service", "agency", "consult", "done-for-you"]):
        return "productized service"
    if any(term in normalized for term in ["software", "saas", "app", "tool", "automation platform"]):
        return "micro-saas"
    if any(term in normalized for term in ["course", "guide", "template", "newsletter", "content"]):
        return "digital product and opt-in audience"
    if any(term in normalized for term in ["marketplace", "listing", "ecommerce", "catalog"]):
        return "marketplace optimization"
    return "compliant venture experiment"


def build_first_actions(lane: str) -> list[str]:
    shared = [
        "Run the idea through docs/policies/compliance_pack.md and confirm the data source is consented and documented.",
        "Define a narrow customer profile and one concrete value proposition.",
        "Create a landing page or intake form that captures explicit opt-in where personal data is collected.",
    ]

    lane_actions = {
        "productized service": [
            "Package a fixed-scope offer with a clear outcome, price, and delivery timeline.",
            "Collect 3 to 5 proof points or case studies from legitimate prior work.",
        ],
        "micro-saas": [
            "Validate the core workflow with 5 user interviews before building automations at scale.",
            "Instrument signup, activation, and retention events from the start.",
        ],
        "digital product and opt-in audience": [
            "Publish a lead magnet that solves one small problem and captures voluntary subscribers.",
            "Draft a simple email sequence that delivers value first and includes easy opt-out.",
        ],
        "marketplace optimization": [
            "Choose one marketplace and review its seller and automation policies.",
            "Test one listing, offer, or fulfillment loop before expanding.",
        ],
        "compliant venture experiment": [
            "Write a one-page experiment brief with hypothesis, distribution channel, and success threshold.",
            "Keep the first experiment manual until legality and unit economics are proven.",
        ],
    }
    return shared + lane_actions.get(lane, [])


def build_success_metrics(lane: str) -> list[str]:
    baseline = [
        "Positive gross margin on the first paid cohort.",
        "Documented consent rate for every personal-data collection point.",
        "No platform-policy violations, abuse complaints, or deliverability incidents.",
    ]

    lane_metrics = {
        "productized service": [
            "Qualified discovery calls booked per week.",
            "Proposal-to-close conversion rate.",
        ],
        "micro-saas": [
            "Activation rate from signup to first value.",
            "Weekly retained active accounts.",
        ],
        "digital product and opt-in audience": [
            "Lead magnet conversion rate.",
            "Revenue per subscriber and unsubscribe rate.",
        ],
        "marketplace optimization": [
            "Listing conversion rate.",
            "Contribution margin after fees and fulfillment.",
        ],
        "compliant venture experiment": [
            "Experiment cycle time.",
            "Evidence quality for each hypothesis.",
        ],
    }
    return baseline + lane_metrics.get(lane, [])


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())
