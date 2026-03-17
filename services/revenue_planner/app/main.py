from fastapi import FastAPI

from . import schemas
from .services.planner import (
    generate_revenue_plan,
    assess_strategy_risk,
    list_safe_revenue_tracks,
)

app = FastAPI(
    title="Revenue Planner Service",
    description="Generates compliant, redundant autonomous revenue plans.",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tracks")
async def get_tracks() -> list[dict[str, str]]:
    return list_safe_revenue_tracks()


@app.get("/plans/schema")
async def get_plan_schema() -> dict:
    return schemas.RevenuePlanRequest.model_json_schema()


@app.post("/plans", response_model=schemas.RevenuePlanResponse)
async def create_revenue_plan(
    payload: schemas.RevenuePlanRequest,
) -> schemas.RevenuePlanResponse:
    return generate_revenue_plan(payload)


@app.post("/assess-risk", response_model=schemas.StrategyRiskResponse)
async def create_risk_assessment(
    payload: schemas.StrategyRiskRequest,
) -> schemas.StrategyRiskResponse:
    return assess_strategy_risk(payload)
