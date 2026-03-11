# Agentic Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Implement Gmail OAuth ingestion instrument with sender/recipient/cc extraction and provenance tags | Data Operations Agent | Must enforce account-owner authorization and store consent state |
| P0 | Add compliance gate extension that blocks outreach to `consent_status != explicit/implied` | Compliance Guardian | Hard-stop before campaign execution |
| P0 | Build dedupe + suppression pipeline (revoked, bounced, unsubscribed) | Data Operations Agent | Required for deliverability and legal posture |
| P1 | Launch first compliant monetization loop (newsletter + affiliate CTA) | Growth Agent | Track CTR, conversion, and unsubscribe rate |
| P1 | Create KPI dashboard for funnel, revenue, and campaign health | Orchestrator + Telemetry Sentinel | Feed weekly mission review |
| P1 | Stand up paper-trading research harness with strategy scorecard | Trading Research Agent | No live funds until acceptance criteria met |
| P2 | Automate weekly payout/reconciliation checklist for transfer ledger | Finance Ops Agent | Include transfer verification to target account workflow |
| P2 | Produce tutorial outline + YouTube narrative storyboard with mascot character bible | Content Studio Agent | Reuse mission diary as source material |
