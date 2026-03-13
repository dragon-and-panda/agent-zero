# Agentic Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build Gmail ingestion connector with OAuth least-privilege scopes and consent ledger integration | Data Steward | Block extraction when consent status is unknown for outbound use |
| P0 | Implement contact normalization and deduplication pipeline (header parsing + entity merge) | Toolsmith | Include deterministic merge keys + confidence scoring |
| P0 | Create RAG retrieval layer for audience intelligence queries and campaign planning | Toolsmith | Retrieval must include consent filter predicates |
| P1 | Add Orange workflow templates for segmentation, anomaly detection, and audience scoring | Revenue Operator | Export scored cohorts back to orchestrator with audit metadata |
| P1 | Launch first monetization experiment stack (newsletter + affiliate + sponsorship tracking) | Revenue Operator | Permission-based only; track CAC, conversion, and churn |
| P1 | Implement treasury auto-allocation and payout reconciliation pipeline to `$Nicsins` | Treasury Agent | Requires reconciliation and reserve checks before transfer |
| P2 | Define paper-trading harness and risk gates before any live Forex allocation | Risk Controller | Require positive simulation metrics and drawdown limits |
| P2 | Build content engine templates for tutorial lessons and YouTube script generation | Story Architect | Include consistent narrator persona and visual style bible |
