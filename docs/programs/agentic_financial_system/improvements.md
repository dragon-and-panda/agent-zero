# Agentic Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build Gmail OAuth inbox-ingestion service with consent ledger and audit logging | Inbox Intelligence Agent | Include token rotation, scope minimization, and revoke flow |
| P0 | Implement entity normalization and dedupe for From/To/Cc contact graphs | Data Quality Agent | Must support alias merge and suppression lists |
| P0 | Stand up RAG index for campaign planning and account intelligence | Data Platform Agent | Restrict chunking to policy-safe metadata and snippets |
| P1 | Create Orange DataScaping workflow templates for segmentation QA | Analytics Agent | Export reproducible segment definitions, not raw personal-data dumps |
| P1 | Launch first consent-based offer funnel (landing page + qualification + CRM handoff) | Offer Architect | Track lead quality and conversion by source |
| P1 | Deploy deliverability and compliance monitors (unsubscribe, complaint, bounce thresholds) | Compliance Sentinel | Auto-halt campaigns when thresholds are breached |
| P2 | Build treasury ledger + payout checklist automation for `$Nicsins` transfers | Capital Orchestrator | Keep human approval gate for external transfers |
| P2 | Implement trading-lab sandbox (backtests, paper trading, drawdown alerts) | Strategy Researcher | No live capital until readiness gates are met |
| P2 | Create course production pipeline and episode script templates | Story Producer | Connect each episode to mission KPIs and retrospective logs |
