# Agentic Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build Gmail metadata ingestion pipeline with provenance tags (`received`, `sent`, `cc`, `file_import`) | Data Steward | OAuth least-privilege scopes; normalize headers only in MVP |
| P0 | Implement consent/suppression classifier (`opt_in`, `business_public`, `unknown`, `do_not_contact`) | Compliance Sentinel | Block outbound flows for non-compliant segments |
| P0 | Create first opt-in funnel and lead magnet offer | Revenue Builder | Focus on inbound, consent-based list growth |
| P1 | Add Orange DataScaping workflow templates for segmentation and campaign analysis | Analytics Curator | Use anonymized identifiers where possible |
| P1 | Build treasury ledger and transfer proof archive workflow | Treasury Operator | Reconcile revenue, fees, refunds, net cashflow |
| P1 | Add KPI dashboard (WRR, CPQL, conversion, unsubscribe, drawdown) | Telemetry Sentinel | Daily snapshots + weekly trend summaries |
| P2 | Stand up Forex strategy lab (backtest + paper trade evaluator) | Trading Analyst | Enforce risk gates before any live deployment |
| P2 | Build content pipeline for course modules and YouTube scripts | Narrative Producer | Tie each sprint output to one educational artifact |
