# Agentic Financial System — Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Implement consent ledger (`contact_id`, source, opt-in proof, timestamp, scope) | Data Steward | Required before outreach automations |
| P0 | Implement suppression/unsubscribe workflow across all outbound channels | Data Steward | Must be enforced at send time |
| P0 | Build Gmail authorized ingestion + header parser for From/To/CC metadata | Toolsmith | OAuth + least privilege only |
| P1 | Build RAG index over approved message corpus with provenance tags | Toolsmith | Support retrieval filtering by consent scope |
| P1 | Orange segmentation pipeline for dedupe, clustering, and quality scoring | Revenue Operator | Inputs should exclude restricted contacts |
| P1 | Launch first opt-in lead magnet funnel + analytics events | Revenue Operator | Track CAC, CVR, and unsubscribe rate |
| P2 | Add weekly payout reconciliation SOP and transfer checklist for `$Nicsins` | Apex Orchestrator | Include audit log and exception handling |
| P2 | Stand up paper-trading harness with risk telemetry dashboard | Risk Controller | No live capital until acceptance criteria pass |
| P2 | Automate content transformation: logs -> tutorial module -> YouTube script | Content Studio | Add recurring narrator arc template |
