### revenue_planning
screen and structure monetization ideas before execution
use it when a task involves making money, new ventures, lead generation, outreach, data acquisition, automation for sales, or business model selection

hard rules:
- reject plans that depend on selling personal data, scraping private inboxes, spam, account abuse, platform circumvention, or unclear data provenance
- prefer opt-in, first-party, contract-backed, and platform-compliant workflows
- return a lane, verdict, rationale, and next actions the agent can execute lawfully

usage:
~~~json
{
    "thoughts": [
        "...",
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "objective": "Create an autonomous revenue lane for local service lead generation.",
        "constraints": "Must use consented first-party data and comply with email/platform rules.",
        "idea": "Use landing pages, inbound qualification, and CRM enrichment for opted-in prospects."
    }
}
~~~
