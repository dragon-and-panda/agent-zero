from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class AutomationMaturity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RiskTolerance(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RevenueTrackId(str, Enum):
    productized_service = "productized_service"
    digital_product = "digital_product"
    marketplace_listings = "marketplace_listings"
    affiliate_content = "affiliate_content"
    recurring_retainer = "recurring_retainer"


class RevenuePlanRequest(BaseModel):
    mission_name: str = Field(
        "ethical revenue engine",
        description="Working name for the revenue mission.",
    )
    cash_on_hand: float = Field(
        0,
        ge=0,
        description="Liquid funds available for launch and experiments.",
    )
    weekly_hours: int = Field(
        10,
        ge=1,
        le=168,
        description="Hours available each week for launch and operations.",
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Current skills, domain expertise, and delivery capabilities.",
    )
    existing_assets: List[str] = Field(
        default_factory=list,
        description="Existing channels, audiences, software, content, or inventory.",
    )
    preferred_tracks: List[RevenueTrackId] = Field(
        default_factory=list,
        description="Tracks the operator wants to prioritize if viable.",
    )
    proposed_tactics: List[str] = Field(
        default_factory=list,
        description="Specific tactics to assess for legality, ethics, and platform risk.",
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Hard limits such as no paid ads, no shipping, or no live sales calls.",
    )
    avoided_tactics: List[str] = Field(
        default_factory=list,
        description="Tactics the operator does not want to use.",
    )
    automation_maturity: AutomationMaturity = Field(
        AutomationMaturity.medium,
        description="How capable the current stack is at running repeatable automations.",
    )
    risk_tolerance: RiskTolerance = Field(
        RiskTolerance.low,
        description="Operating risk tolerance for experiments and channel concentration.",
    )
    audience_size: int = Field(
        0,
        ge=0,
        description="Approximate first-party audience size across owned channels.",
    )
    real_capital_trading_enabled: bool = Field(
        False,
        description="Whether the operator intends to allocate real capital to trading research.",
    )


class RejectedTactic(BaseModel):
    tactic: str
    severity: str = Field(description="high | medium")
    reason: str
    compliant_replacement: str


class RevenueTrackRecommendation(BaseModel):
    track_id: RevenueTrackId
    label: str
    score: int = Field(ge=0, le=100)
    why_now: str
    startup_cost: str
    automation_fit: str
    dependency_risk: str
    first_actions: List[str] = Field(default_factory=list)
    backup_if_blocked: str


class PhasePlan(BaseModel):
    phase: str
    objective: str
    entry_criteria: str
    success_checks: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)


class ContingencyRule(BaseModel):
    trigger: str
    response: str
    fallback: str


class KpiTarget(BaseModel):
    name: str
    target: str
    why: str


class RevenuePlanResponse(BaseModel):
    mission_name: str
    summary: str
    hard_guardrails: List[str] = Field(default_factory=list)
    rejected_tactics: List[RejectedTactic] = Field(default_factory=list)
    primary_tracks: List[RevenueTrackRecommendation] = Field(default_factory=list)
    backup_tracks: List[RevenueTrackRecommendation] = Field(default_factory=list)
    phases: List[PhasePlan] = Field(default_factory=list)
    contingency_rules: List[ContingencyRule] = Field(default_factory=list)
    kpi_targets: List[KpiTarget] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class StrategyRiskRequest(BaseModel):
    summary: str = Field(..., description="High-level strategy summary to inspect.")
    tactics: List[str] = Field(default_factory=list, description="Concrete tactics to inspect.")


class StrategyRiskResponse(BaseModel):
    is_allowed: bool
    rejected_tactics: List[RejectedTactic] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
