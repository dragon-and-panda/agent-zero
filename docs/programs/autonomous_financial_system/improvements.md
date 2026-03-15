# Autonomous Financial System - Improvement Backlog

| Priority | Opportunity | Owner Agent | Notes |
| --- | --- | --- | --- |
| P0 | Implement Gmail ingestion pipeline with OAuth + least-privilege scopes | Toolsmith | Include robust retry, pagination, and schema validation |
| P0 | Add consent-state engine (`opt_in`/`opt_out`/`unknown`) and suppression rules | Data Steward | Must block outbound messaging for unknown or opted-out contacts |
| P0 | Build contact normalization + deduplication graph across To/From/Cc sources | Data Steward | Include domain-level enrichment and collision handling |
| P1 | Add RAG indexing pipeline for approved email/file content | Toolsmith | Chunking, embeddings, retrieval QA metrics |
| P1 | Integrate Orange DataScaping segmentation workflow | Monetization Operator | Segment by intent/engagement; no resale-list outputs |
| P1 | Launch first compliant monetization experiment (newsletter or client service) | Monetization Operator | Define funnel, offer, and success threshold |
| P2 | Create weekly KPI dashboard template (revenue, CAC, consent rate, engagement) | Mission Orchestrator | Include auto-generated retrospective section |
| P2 | Stand up paper-trading journal and risk policy enforcement checks | Risk Controller | Trading disabled until reserve + governance criteria are met |
| P2 | Build tutorial content pipeline (capture -> script -> publish) | Content Producer | Reuse mission diary entries as source material |
| P3 | Produce anthropomorphic narrator character kit (visual, tone, story arc) | Content Producer | Align with "mech suit/robot body" narrative theme |
