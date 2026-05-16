### revenue_planning:
screen monetization ideas before acting on them
use for revenue plans involving inboxes, gmail, contacts, outreach, marketplaces, or data extraction
reject personal-data resale and convert to compliant alternatives

common inputs:
- proposal: plain-language description of the idea
- lane: short label for the business lane
- data_sources: where the data comes from
- automation_plan: what the agent will automate
- monetization_model: how money is earned
- consent_status: describe opt-in or permission quality
- provenance: describe data ownership and documentation quality
- platform_rules: describe tos or marketplace rule confidence
- owner_authorized: true only when the mailbox or system owner explicitly authorized the workflow
- notes: extra context

usage:
~~~json
{
    "thoughts": [
        "This touches monetization and contact data, so I should screen it before proceeding."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "proposal": "Use an owner-authorized inbox to classify inbound leads and sync them into the client's CRM.",
        "lane": "client-owned inbox operations",
        "data_sources": "client mailbox and CRM",
        "automation_plan": "summarize, classify, deduplicate, and route inbound leads",
        "monetization_model": "monthly retained service",
        "consent_status": "high",
        "provenance": "high",
        "platform_rules": "high",
        "owner_authorized": true
    }
}
~~~
