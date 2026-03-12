# Agentic Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build Gmail OAuth ingestion instrument with least-privilege scopes and incremental sync | Toolsmith Agent | Must include provenance metadata and message ID dedupe |
| P0 | Add consent/provenance schema (`opt_in`, `existing_relationship`, `public_business`, `blocked`) to contact master table | Data Steward | Required before any outbound usage |
| P0 | Create suppression list automation and pre-send compliance check | Data Steward | Hard fail campaign export when blocked contacts are present |
| P1 | Integrate Orange DataScaping workflow (CSV export + segment scoring round-trip) | Monetization Analyst | Standardize segment naming and confidence scores |
| P1 | Launch first opt-in funnel + newsletter sponsorship pipeline | Monetization Analyst | Replace any list-broker concept with permission-based growth |
| P1 | Build revenue ledger and automated distribution report for Cash App transfer reconciliation | Risk Controller | Include tax reserve and operating reserve allocation |
| P2 | Add trading simulation journal with strategy metrics (expectancy, drawdown, hit rate) | Risk Controller | No live trading until preconditions are met |
| P2 | Produce first course module + YouTube script package featuring Alloy Fox narrative arc | Content Director | Tie narrative to real KPIs and transparent postmortems |
