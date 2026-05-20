### revenue_planning:
screen a proposed revenue lane before building or automating it
use when tasks mention monetization, lead generation, outreach, inbox data, customer acquisition, or platform-based revenue
this tool checks legality, consent, data provenance, and platform risk first
reject plans that depend on privacy abuse, personal-data resale, spam, or weak provenance
prefer this tool before building a business workflow when the safety or legality is unclear
usage:
~~~json
{
    "thoughts": [
        "I should screen this monetization idea before acting on it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "idea": "First-party inbox-to-CRM service for authorized clients",
        "offer": "CRM cleanup and follow-up summaries",
        "customer": "small businesses",
        "acquisition": "direct consulting",
        "legality": "high",
        "consent": "high",
        "data_provenance": "high",
        "platform_risk": "low",
        "time_to_revenue": "medium",
        "margin": "high",
        "repeatability": "medium",
        "automation": "high",
        "defensibility": "medium",
        "notes": "No personal-data resale."
    }
}
~~~
