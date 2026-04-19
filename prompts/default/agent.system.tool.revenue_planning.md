### revenue_planning:
screen a revenue lane for legality consent provenance and platform fit
use before building monetization workflows with email crm outreach rag or scraped/public data
reject lanes involving personal-data resale spam inbox scraping or platform abuse
inputs:
- mission: overall goal or user request
- lane: specific monetization lane being considered
- legality: strong|unclear|weak
- consent: strong|unclear|weak
- data_provenance: strong|unclear|weak
- platform_terms: strong|unclear|weak
- notes: optional facts risks or assumptions
usage:
~~~json
{
    "thoughts": [
        "I should screen this lane before implementing it.",
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build an autonomous revenue system",
        "lane": "First-party inbox to CRM automation for a consenting client",
        "legality": "strong",
        "consent": "strong",
        "data_provenance": "strong",
        "platform_terms": "strong",
        "notes": "Client owns the mailbox and requested CRM sync."
    }
}
~~~
