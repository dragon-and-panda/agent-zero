### revenue_planning

screen monetization ideas before execution
use for business models, lead-gen plans, data-use questions, or revenue workflows that may touch compliance, privacy, or platform rules
provide ratings using low medium high

hard gates:
- legality
- consent
- data_provenance
- platform_compliance

soft factors:
- time_to_cash
- margin
- repeatability
- automation_fit
- defensibility

the tool returns PASS HOLD or REJECT with reasons and safer pivots

example usage
~~~json
{
  "thoughts": [
    "This is a monetization workflow and I should screen it before acting."
  ],
  "tool_name": "revenue_planning",
  "tool_args": {
    "mission": "Build an owner-authorized inbox-to-CRM workflow for a small business",
    "revenue_model": "Managed service and software subscription",
    "data_sources": "Business-owned Gmail inbox and CRM exports",
    "channels": "Internal CRM and analytics dashboard",
    "legality": "high",
    "consent": "high",
    "data_provenance": "high",
    "platform_compliance": "high",
    "time_to_cash": "medium",
    "margin": "high",
    "repeatability": "high",
    "automation_fit": "high",
    "defensibility": "medium",
    "notes": "Outputs stay internal and are not sold as contact lists."
  }
}
~~~
