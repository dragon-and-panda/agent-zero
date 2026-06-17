### revenue_planning

screen a monetization idea before acting on it
use for venture selection, growth experiments, and autonomous revenue planning
do not use it to justify privacy abuse, spam, or personal-data resale

required ratings:
- legality
- consent
- provenance
- tos
- margin
- repeatability
- automation
- defensibility
- time_to_cash
- setup_complexity

all ratings must be one of: low, medium, high

usage:
~~~json
{
    "thoughts": [
        "Need to screen the idea before spending build effort.",
        "I should rate the lane on compliance and commercial quality first."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "opportunity": "Inbox-to-CRM automation for opt-in operators",
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "tos": "high",
        "margin": "medium",
        "repeatability": "high",
        "automation": "high",
        "defensibility": "medium",
        "time_to_cash": "medium",
        "setup_complexity": "medium",
        "notes": "First-party workflow sold directly to the inbox owner."
    }
}
~~~
