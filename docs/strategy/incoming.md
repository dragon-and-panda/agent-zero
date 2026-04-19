# Strategy Intake Queue

Use this queue for new revenue ideas before execution. Every entry should be scored, documented, and either activated, held, or rejected.

## Intake template

| Lane | Summary | Data source | Consent status | Platform fit | Score status | Decision | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Inbox-to-CRM operations | Organize and enrich a consenting customer's own inbound contacts and follow-ups. | Customer-owned inbox and CRM exports | Explicit customer authorization required | Strong if scoped to owned systems | PASS candidate | Active priority | Lowest compliance risk and fast service delivery path |
| Autonomous listing service | Create and manage listings for inventory the customer owns or is authorized to sell. | Customer photos, notes, and marketplace data used per platform rules | Customer authorization required | Strong with channel-specific rules | PASS candidate | Active hedge | See `docs/autonomous_listing_service.md` |
| Research brief product | Produce benchmark reports from public, licensed, or user-provided sources. | Public web, licensed databases, user uploads | Not personal-data driven | Strong if claims are sourced | PASS candidate | Active hedge | Good fit for RAG and repeatable templates |
| Productized agent workflows | Sell setup, customization, and operations support around Agent Zero-based automations. | Repo knowledge, user requirements, public docs | Customer engagement is explicit | Strong | PASS candidate | Active hedge | Can compound into services and templates |
| Contact-list brokerage | Scrape or compile personal email lists and sell them. | Personal contact data of third parties | No meaningful consent | Weak and high-risk | REJECT | Rejected | Violates `docs/policies/compliance_pack.md` |
