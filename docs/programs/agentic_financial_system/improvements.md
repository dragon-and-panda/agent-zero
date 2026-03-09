# Agentic Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Build authorized Gmail connector with OAuth token handling and source-level consent tracking | Data Steward | Ingest headers only by default; content fetch requires explicit opt-in scope |
| P0 | Add contact normalization + de-duplication pipeline (From/To/Cc/Bcc) | Data Steward | Include suppression flags, legal-use tags, and retention timestamps |
| P0 | Create Orange DataScaping workflow for segmentation and quality scoring | Growth Operator | Start with synthetic dataset before connecting live records |
| P1 | Implement experiment board for monetization channels (sponsorship, affiliate, services, digital products) | Growth Operator | Weekly cohort scoring and kill/scale rules |
| P1 | Add treasury ledger template with transfer reconciliation to `$Nicsins` | Treasury Controller | Manual transfer verification + audit trail |
| P1 | Define trading readiness checklist and paper-trading validation suite | Treasury Controller | No live trading until checklist complete |
| P2 | Build content pipeline templates (docs -> course module -> video script) | Story Producer | Include narrator persona consistency guide |
| P2 | Add KPI snapshot automation for daily/weekly review | Apex Orchestrator | Publish to logs and mission diary summary |
