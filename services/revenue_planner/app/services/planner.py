from __future__ import annotations

from dataclasses import dataclass

from .. import schemas


HARD_GUARDRAILS = [
    "Do not extract, compile, or sell private contact data from email or messaging systems.",
    "Use only opt-in, first-party, or clearly authorized data for lead generation and outreach.",
    "Reject spam, deceptive claims, and any workflow that hides consent state or business identity.",
    "Keep experimental capital separate from operating cash and require explicit risk limits for trading research.",
]


@dataclass(frozen=True)
class TrackProfile:
    track_id: schemas.RevenueTrackId
    label: str
    startup_cost: str
    automation_fit: str
    dependency_risk: str
    base_score: int
    skill_keywords: tuple[str, ...]
    asset_keywords: tuple[str, ...]
    first_actions: tuple[str, ...]
    backup_if_blocked: str
    why_template: str


TRACKS = (
    TrackProfile(
        track_id=schemas.RevenueTrackId.productized_service,
        label="Productized service",
        startup_cost="low",
        automation_fit="high",
        dependency_risk="low",
        base_score=68,
        skill_keywords=("design", "automation", "writing", "editing", "ops", "research", "marketing", "development"),
        asset_keywords=("website", "portfolio", "case study", "github", "crm"),
        first_actions=(
            "Define one narrowly scoped offer with a fixed outcome and delivery window.",
            "Publish an intake form and qualifying checklist.",
            "Create a delivery SOP and a post-delivery upsell path.",
        ),
        backup_if_blocked="Convert the service steps into a lower-ticket audit or template pack.",
        why_template="This fits best when skills already exist and cash needs to start quickly without heavy upfront spend.",
    ),
    TrackProfile(
        track_id=schemas.RevenueTrackId.digital_product,
        label="Template / digital product",
        startup_cost="low",
        automation_fit="high",
        dependency_risk="medium",
        base_score=62,
        skill_keywords=("prompt", "template", "spreadsheet", "curriculum", "course", "design", "writing"),
        asset_keywords=("newsletter", "audience", "website", "blog", "youtube", "downloads"),
        first_actions=(
            "Package one repeated deliverable into a template, checklist, or mini-tool.",
            "Create a landing page with an opt-in lead magnet and paid upsell.",
            "Document fulfillment so the asset can be refreshed, not rebuilt.",
        ),
        backup_if_blocked="Bundle the product with a live service or audit to improve conversion.",
        why_template="This track compounds well because each sale strengthens reusable assets and reduces marginal labor.",
    ),
    TrackProfile(
        track_id=schemas.RevenueTrackId.marketplace_listings,
        label="Marketplace listings / resale workflow",
        startup_cost="medium",
        automation_fit="medium",
        dependency_risk="medium",
        base_score=58,
        skill_keywords=("sourcing", "pricing", "photography", "shipping", "copywriting", "negotiation"),
        asset_keywords=("inventory", "storage", "local pickup", "camera", "suppliers"),
        first_actions=(
            "Choose one product category with clear pricing and low return risk.",
            "Standardize listing creation, photo capture, and fulfillment steps.",
            "Use marketplace-native demand first, then add a first-party checkout later.",
        ),
        backup_if_blocked="Switch to consignment, local pickup, or digital listing services if inventory becomes constrained.",
        why_template="This fits teams that can turn operational discipline and listing automation into near-term cash flow.",
    ),
    TrackProfile(
        track_id=schemas.RevenueTrackId.affiliate_content,
        label="Affiliate / educational content",
        startup_cost="low",
        automation_fit="medium",
        dependency_risk="high",
        base_score=50,
        skill_keywords=("writing", "research", "seo", "video", "editing", "teaching"),
        asset_keywords=("newsletter", "youtube", "blog", "social", "community"),
        first_actions=(
            "Pick a narrow buying question and publish comparison-style content around it.",
            "Route traffic into an owned newsletter or resource library.",
            "Track which topics convert before expanding content volume.",
        ),
        backup_if_blocked="Use the same content to sell a direct template, guide, or audit instead of relying only on commissions.",
        why_template="This becomes attractive once first-party distribution exists or educational content can be published consistently.",
    ),
    TrackProfile(
        track_id=schemas.RevenueTrackId.recurring_retainer,
        label="Recurring retainer",
        startup_cost="low",
        automation_fit="medium",
        dependency_risk="medium",
        base_score=55,
        skill_keywords=("ops", "automation", "support", "analytics", "growth", "development"),
        asset_keywords=("case study", "results", "referrals", "crm"),
        first_actions=(
            "Identify one recurring business pain that can be solved each month with a stable SOP.",
            "Define reporting, delivery cadence, and boundaries to avoid custom sprawl.",
            "Use an initial fixed-scope project as the retainer entry point.",
        ),
        backup_if_blocked="Keep a one-off version of the offer available so cash flow does not depend on closing retainers immediately.",
        why_template="Retainers stabilize cash flow once an initial proof-of-work exists and delivery is already systematized.",
    ),
)


DISALLOWED_TACTICS = {
    "sell email lists": (
        "Selling contact lists harvested from personal or third-party communications creates major privacy, spam, and platform-compliance risk.",
        "Build opt-in lead magnets, newsletters, or quote-request funnels instead.",
    ),
    "email list": (
        "Unqualified email-list monetization often implies consent problems unless the contacts explicitly opted in for that purpose.",
        "Use first-party lead capture with stored consent and source attribution.",
    ),
    "gmail": (
        "Mining private inboxes for monetization targets crosses privacy and authorization boundaries.",
        "Restrict email use to your own lawful business workflows and opt-in contact management.",
    ),
    "cc": (
        "Harvesting addresses from CC lines or message headers is not a compliant lead-generation method.",
        "Use on-site forms, customer referrals, and marketplace-native inquiries.",
    ),
    "scrap": (
        "Scraping personal contact data or platform-protected user data risks legal and terms-of-service violations.",
        "Collect permissioned first-party data and public business information used within platform rules.",
    ),
    "spam": (
        "Spam tactics degrade deliverability and create legal exposure.",
        "Use consent-based outreach and value-first content funnels.",
    ),
}


def _contains_keyword(text: str, keyword: str) -> bool:
    return keyword in text.lower()


def assess_strategy_risk(request: schemas.StrategyRiskRequest) -> schemas.StrategyRiskResponse:
    text = " ".join([request.summary, *request.tactics]).lower()
    rejected: list[schemas.RejectedTactic] = []

    for keyword, (reason, replacement) in DISALLOWED_TACTICS.items():
        if _contains_keyword(text, keyword):
            rejected.append(
                schemas.RejectedTactic(
                    tactic=keyword,
                    severity="high",
                    reason=reason,
                    compliant_replacement=replacement,
                )
            )

    if "forex" in text or "trading" in text:
        rejected.append(
            schemas.RejectedTactic(
                tactic="real-capital speculative trading",
                severity="medium",
                reason="Speculative trading should not be treated as a primary revenue engine before operating cash flow, written risk limits, and paper-trading validation exist.",
                compliant_replacement="Keep trading in research mode first and prioritize cash-generating offers with controllable unit economics.",
            )
        )

    return schemas.StrategyRiskResponse(
        is_allowed=not rejected,
        rejected_tactics=rejected,
        notes=[
            "Permissioned first-party data, clear disclosures, and channel redundancy should be mandatory.",
        ],
    )


def list_safe_revenue_tracks() -> list[dict[str, str]]:
    return [
        {
            "track_id": track.track_id.value,
            "label": track.label,
            "startup_cost": track.startup_cost,
            "automation_fit": track.automation_fit,
            "dependency_risk": track.dependency_risk,
            "why": track.why_template,
        }
        for track in TRACKS
    ]


def _score_track(request: schemas.RevenuePlanRequest, track: TrackProfile) -> int:
    score = track.base_score
    skill_blob = " ".join(request.skills).lower()
    asset_blob = " ".join(request.existing_assets).lower()
    constraint_blob = " ".join(request.constraints + request.avoided_tactics).lower()

    if any(keyword in skill_blob for keyword in track.skill_keywords):
        score += 10
    if any(keyword in asset_blob for keyword in track.asset_keywords):
        score += 8
    if track.track_id in request.preferred_tracks:
        score += 6

    if request.cash_on_hand < 250 and track.startup_cost == "low":
        score += 6
    if request.weekly_hours <= 10 and track.automation_fit == "high":
        score += 5
    if request.weekly_hours >= 20 and track.track_id in {
        schemas.RevenueTrackId.productized_service,
        schemas.RevenueTrackId.marketplace_listings,
    }:
        score += 4
    if request.audience_size > 250 and track.track_id in {
        schemas.RevenueTrackId.digital_product,
        schemas.RevenueTrackId.affiliate_content,
    }:
        score += 7
    if request.automation_maturity == schemas.AutomationMaturity.high and track.automation_fit == "high":
        score += 4
    if request.risk_tolerance == schemas.RiskTolerance.low and track.dependency_risk == "high":
        score -= 8
    if "no shipping" in constraint_blob and track.track_id == schemas.RevenueTrackId.marketplace_listings:
        score -= 10
    if "no calls" in constraint_blob and track.track_id == schemas.RevenueTrackId.recurring_retainer:
        score -= 4
    if "no audience work" in constraint_blob and track.track_id == schemas.RevenueTrackId.affiliate_content:
        score -= 8

    return max(0, min(score, 100))


def _make_recommendation(request: schemas.RevenuePlanRequest, track: TrackProfile) -> schemas.RevenueTrackRecommendation:
    score = _score_track(request, track)
    return schemas.RevenueTrackRecommendation(
        track_id=track.track_id,
        label=track.label,
        score=score,
        why_now=track.why_template,
        startup_cost=track.startup_cost,
        automation_fit=track.automation_fit,
        dependency_risk=track.dependency_risk,
        first_actions=list(track.first_actions),
        backup_if_blocked=track.backup_if_blocked,
    )


def generate_revenue_plan(request: schemas.RevenuePlanRequest) -> schemas.RevenuePlanResponse:
    risk = assess_strategy_risk(
        schemas.StrategyRiskRequest(
            summary=request.mission_name,
            tactics=request.proposed_tactics,
        )
    )

    ranked = sorted(
        (_make_recommendation(request, track) for track in TRACKS),
        key=lambda item: item.score,
        reverse=True,
    )
    primary_tracks = ranked[:2]
    backup_tracks = ranked[2:3]

    phases = [
        schemas.PhasePlan(
            phase="phase_0_foundation",
            objective="Select compliant offers, define guardrails, and instrument the scoreboard.",
            entry_criteria="Mission approved and operator resources inventoried.",
            success_checks=[
                "Two primary tracks and one backup track selected.",
                "Offer scope, intake path, and KPI dashboard defined.",
                "Disallowed tactics replaced with compliant alternatives.",
            ],
            next_actions=[
                "Turn the best track into a fixed-scope offer or product page.",
                "Create an opt-in or marketplace-native intake path.",
                "Set weekly review cadence for leads, cash collected, and fulfillment time.",
            ],
        ),
        schemas.PhasePlan(
            phase="phase_1_launch",
            objective="Start collecting cash from the primary track while documenting delivery.",
            entry_criteria="Offer page, intake, and delivery SOP exist.",
            success_checks=[
                "First paying customer or first validated marketplace sale completed.",
                "Delivery time captured and bottlenecks identified.",
                "Each completed job produces at least one reusable asset.",
            ],
            next_actions=[
                f"Launch {primary_tracks[0].label.lower()} first.",
                f"Keep {primary_tracks[1].label.lower()} as a parallel channel to reduce concentration risk.",
                "Convert frequent objections into FAQ, content, and template improvements.",
            ],
        ),
        schemas.PhasePlan(
            phase="phase_2_redundancy",
            objective="Reduce failure risk by duplicating acquisition and fulfillment paths.",
            entry_criteria="At least one track has early proof of demand.",
            success_checks=[
                "Each active offer has at least two acquisition channels.",
                "Backup offer can be activated within one working session.",
                "Operating cash is separated from experimental spending.",
            ],
            next_actions=[
                "Add a second channel for the working offer.",
                "Automate repetitive delivery, reporting, or publishing steps.",
                "Promote successful workflows into templates, SOPs, and tutorials.",
            ],
        ),
    ]

    if request.real_capital_trading_enabled:
        phases.append(
            schemas.PhasePlan(
                phase="phase_3_capital_research",
                objective="Treat trading as capped research with paper-trading evidence and written risk limits.",
                entry_criteria="Core offer revenue is stable and drawdown policy is documented.",
                success_checks=[
                    "Paper-trading logs show repeatable behavior.",
                    "Max drawdown, max size, and stop conditions are defined.",
                    "Research capital remains separate from operating cash.",
                ],
                next_actions=[
                    "Keep position sizing minimal and review metrics weekly.",
                    "Do not expand capital allocation without documented controls.",
                ],
            )
        )

    return schemas.RevenuePlanResponse(
        mission_name=request.mission_name,
        summary=(
            "Build revenue from compliant, first-party, and operationally controllable channels "
            "while maintaining at least one backup path and explicit guardrails."
        ),
        hard_guardrails=HARD_GUARDRAILS,
        rejected_tactics=risk.rejected_tactics,
        primary_tracks=primary_tracks,
        backup_tracks=backup_tracks,
        phases=phases,
        contingency_rules=[
            schemas.ContingencyRule(
                trigger="Primary acquisition channel drops below target conversion for two review cycles.",
                response="Pause expansion spend and shift focus to the secondary track.",
                fallback="Promote a lower-friction lead magnet or lower-ticket self-serve offer.",
            ),
            schemas.ContingencyRule(
                trigger="Fulfillment time exceeds the promised window.",
                response="Narrow scope, raise price, or route demand into a waitlist.",
                fallback="Sell templates, audits, or async deliverables until operations recover.",
            ),
            schemas.ContingencyRule(
                trigger="Compliance or consent ambiguity appears in a data workflow.",
                response="Stop the workflow immediately and replace the tactic with opt-in collection.",
                fallback="Use content, referrals, or marketplace-native demand instead of contact harvesting.",
            ),
        ],
        kpi_targets=[
            schemas.KpiTarget(
                name="channel_concentration",
                target="No single acquisition channel > 70% of total demand once redundancy phase begins.",
                why="Limits platform and algorithm dependency.",
            ),
            schemas.KpiTarget(
                name="lead_to_cash_cycle_time",
                target="Track weekly and reduce with SOP and automation improvements.",
                why="Faster cycles improve learning and reinvestment speed.",
            ),
            schemas.KpiTarget(
                name="reusable_asset_output",
                target="At least one reusable asset created from every completed sale or experiment.",
                why="Compounding assets make the system more autonomous over time.",
            ),
        ],
        notes=[
            "Private-email harvesting and list sales are intentionally excluded from this framework.",
            "Owned audiences and first-party consent are strategic assets; treat them as infrastructure.",
        ],
    )
