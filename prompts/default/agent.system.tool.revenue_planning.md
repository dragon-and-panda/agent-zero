### revenue_planning

Screen a monetization idea before acting on it.

Use this tool when a task involves:

- new revenue lanes;
- growth or monetization strategy;
- automation that touches inboxes, contacts, or private data;
- outreach or lead generation design;
- deciding whether a plan should PASS, HOLD, or REJECT.

This tool is especially important when a request could drift into privacy abuse, weak consent, personal-data resale, spam, or platform evasion.

usage:
~~~json
{
    "thoughts": [
        "I should screen this lane for legality, consent, provenance, and platform alignment before doing any execution work."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "strategy": "Inbox-to-CRM assistant for consenting founders",
        "revenue_model": "monthly subscription plus setup fee",
        "data_sources": "user-connected Gmail inbox and CRM records",
        "channel": "official API integrations",
        "notes": "first-party data only, explicit authorization, reversible pilot"
    }
}
~~~
