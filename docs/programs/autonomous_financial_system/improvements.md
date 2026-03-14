# Autonomous Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Success Metric |
| --- | --- | --- | --- |
| P0 | Build Gmail OAuth ingestion instrument with least-privilege scopes and mailbox segment filters | Toolsmith Agent | 100% ingestion runs include scope + account audit metadata |
| P0 | Implement contact provenance schema (`source`, `consent_status`, `last_verified_at`) | Data Governance Agent | 0 contacts in active audiences without consent status |
| P0 | Add compliance gate that blocks non-consented outreach exports | Compliance Guardian | 0 blocked violations reaching execution stage |
| P1 | Integrate Orange DataScaping pipeline for dedupe + segmentation quality reports | Data Governance Agent | Duplicate rate < 2%, segmentation QA report on each run |
| P1 | Launch first monetization experiments (sponsorship + affiliate + service offer) | Revenue Agent | At least one channel positive contribution margin |
| P1 | Add weekly KPI digest (MRR, CAC, conversion, churn, list growth quality) | Apex Orchestrator | Weekly dashboard delivered on schedule |
| P2 | Stand up paper-trading sandbox with strict strategy validation criteria | Risk Agent | 0 live trades before strategy passes validation gates |
| P2 | Build content pipeline from diary entries -> course modules -> video scripts | Story Agent | Publish first complete module pack and script batch |
