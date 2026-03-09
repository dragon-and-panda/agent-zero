# Agentic Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build Gmail ingestion connector with OAuth, consent labels, and header-only mode | Data Steward | Start with metadata extraction (`From`, `To`, `Cc`, timestamp) and policy checks |
| P0 | Create contact hygiene pipeline (normalize, dedupe, suppressions) | Data Steward | Output `contacts_master.csv`, `consent_verified.csv`, `suppression_list.csv` |
| P0 | Launch first monetization offer with measurable funnel | Monetization Builder | Prefer legal service/product offer over list resale |
| P1 | Integrate Orange workflow artifacts into automated reporting loop | Data Steward | Export segmentation reports to `logs/reports/` |
| P1 | Implement weekly treasury close and allocation checklist | Treasury Clerk | Add transfer and reconciliation evidence logging |
| P1 | Stand up 90-day paper trading tracker with risk breach alerts | Market Operator | No live capital until phase gate passes |
| P2 | Build content production pipeline from journal -> script -> video brief | Narrative Producer | Convert weekly logs into tutorial and YouTube episodes |
| P2 | Add performance dashboard for revenue + drawdown + content metrics | Apex Orchestrator | Single pane view for weekly operating review |
