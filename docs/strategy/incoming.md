# Incoming Revenue Opportunities

Use this queue for raw venture ideas before they enter execution.

| Idea | Data source | Consent status | Platform risk | Initial disposition | Notes |
| --- | --- | --- | --- | --- | --- |
| Seller-authorized listing concierge | Seller-provided assets and notes | Explicit | Medium | PASS candidate | Good fit with `services/autonomous_listing/` and the compliance pack. |
| Premium research digest for a niche | First-party research and licensed sources | Explicit | Low | PASS candidate | Strong recurring revenue potential without personal-data dependency. |
| Owner-authorized Gmail triage and CRM hygiene | First-party Google Workspace or Gmail export owned by the operator | Explicit | Low | PASS candidate | Use RAG for summarization, Orange for analysis, and the consent extractor for any internal contact cleanup. |
| CRM hygiene for an existing business | Owner-authorized first-party CRM export | Explicit | Low | PASS candidate | Allowed when used for internal segmentation, dedupe, and support. |
| Export Gmail contacts and sell them | Inbox-derived personal data | Unknown | High | REJECT | Violates the compliance pack: personal-data resale and unclear consent. |
| Scrape public pages for cold-email blasting | Scraped public contacts | None | High | REJECT | Unsolicited outreach and poor provenance. |

Before work starts:

1. Run `instruments/strategy/score.sh`.
2. Use the `revenue_planning` tool for a structured review.
3. Move only PASS items into an execution program.
