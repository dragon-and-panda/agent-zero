"""
Revenue Planner MCP Server

Exposes deterministic revenue-planning helpers over stdio.
"""

from __future__ import annotations

from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from . import schemas
from .services.planner import (
    assess_strategy_risk as assess_strategy_risk_impl,
    generate_revenue_plan as generate_revenue_plan_impl,
    list_safe_revenue_tracks as list_safe_revenue_tracks_impl,
)

mcp = FastMCP("revenue-planner")


@mcp.tool()
def list_safe_revenue_tracks() -> List[Dict[str, str]]:
    """Return built-in compliant revenue tracks with qualitative metadata."""
    return list_safe_revenue_tracks_impl()


@mcp.tool()
def revenue_plan_request_schema() -> Dict[str, Any]:
    """JSON schema for the revenue plan request payload."""
    return schemas.RevenuePlanRequest.model_json_schema()


@mcp.tool()
def revenue_plan_response_schema() -> Dict[str, Any]:
    """JSON schema for the revenue plan response payload."""
    return schemas.RevenuePlanResponse.model_json_schema()


@mcp.tool()
def strategy_risk_request_schema() -> Dict[str, Any]:
    """JSON schema for the risk-assessment request payload."""
    return schemas.StrategyRiskRequest.model_json_schema()


@mcp.tool()
def assess_strategy_risk(summary: str, tactics: List[str] | None = None) -> Dict[str, Any]:
    """
    Inspect a strategy summary + tactics for privacy, spam, and capital-risk issues.
    """
    result = assess_strategy_risk_impl(
        schemas.StrategyRiskRequest(summary=summary, tactics=tactics or [])
    )
    return result.model_dump(mode="json")


@mcp.tool()
def generate_revenue_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a staged, redundant, guardrail-aware revenue plan.
    """
    request = schemas.RevenuePlanRequest.model_validate(payload)
    result = generate_revenue_plan_impl(request)
    return result.model_dump(mode="json")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
