# Agentic Financial System Improvement Backlog

| Priority | Item | Owner Agent | Status | Notes |
| --- | --- | --- | --- | --- |
| P0 | Add compliance guardrail prompt pack for data privacy + anti-spam rules | Risk & Ethics Governor | Planned | Inject into runtime prompts before any outreach automation. |
| P0 | Implement consent-state schema for contacts (`opt_in`, `unknown`, `dnc`) | Data Operations Agent | Planned | Hard-block monetization when consent is not valid. |
| P0 | Build ingestion adapter spec for Google mail exports + CSV | Data Operations Agent | Planned | Read-only analytics use initially; no mass outreach automation. |
| P0 | Create KPI dashboard definition (MRR, CAC, conversion, churn, cash reserve) | Treasury Agent | Planned | Start with markdown/CSV output, then promote to service endpoint. |
| P1 | Build revenue experiment runner (offer/channel matrix) | Revenue Agent | Planned | Weekly ranking by unit economics and confidence. |
| P1 | Add course production workflow template (SOP -> module -> script -> video) | Content Agent | Planned | Reuse logs and journal entries as source material. |
| P1 | Publish narrator persona guide and visual direction brief | Content Agent | Planned | Character continuity for mech-suit storyline. |
| P1 | Define treasury transfer runbook with reconciliation checklist | Treasury Agent | Planned | Include handling for failed settlement/duplicate transfer prevention. |
| P2 | Add paper-trading simulator ingestion and metric recorder | Treasury Agent | Planned | Gate live deployment behind objective score thresholds. |
| P2 | Prototype dedicated `services/financial_ops` microservice | Platform Engineering | Planned | API for contacts, experiments, and treasury telemetry. |
