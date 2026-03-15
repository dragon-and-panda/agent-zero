# Agentic Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build contact ingestion pipeline with consent classifier (`explicit_opt_in`, `existing_customer_relationship`, `unknown`, `opted_out`) | Data Governance Agent | Must block campaign actions for unknown/opted-out contacts |
| P0 | Add suppression + unsubscribe enforcement and audit trail | Data Governance Agent | Required before any outbound automation |
| P0 | Ship first compliant monetization offer (service package + checkout flow) | Growth Agent | Track conversion funnel and acquisition source |
| P1 | Implement RAG knowledge index for conversation context and segment insights | Toolsmith Agent | Use retrieval for personalization, not list resale |
| P1 | Integrate Orange DataScaping-ready exports (`contacts`, `conversations`, `segments`, `campaign_outcomes`) | Toolsmith Agent | Enables recurring analysis and prioritization |
| P1 | Add KPI dashboard (revenue, CAC payback, complaint rate, unsubscribe rate) | Apex Orchestrator | Daily review cadence |
| P2 | Trading analytics module (backtest + walk-forward + drawdown alerts) | Trading Agent (Advisory) | Keep paper-trading-only until validation gates pass |
| P2 | Treasury reconciliation ledger and transfer approval queue | Apex Orchestrator | Include destination tags and failure handling |
| P2 | Weekly content pipeline (journal -> course chapter -> YouTube script) | Narrative Producer | Tie each episode to real metrics and experiments |

