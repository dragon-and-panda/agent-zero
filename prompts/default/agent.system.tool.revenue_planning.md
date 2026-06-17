### revenue_planning:
evaluate a monetization lane before doing work
use for revenue ideas, ventures, outreach systems, lead gen, offer design, pricing, and prioritization
reject plans involving spam, non-consensual inbox access, personal-data resale, or platform-rule evasion
prefer opt-in demand capture, first-party data, compliance-first operations, and repeatable service delivery
args:
- mission: short description of the proposed lane
- legality: "low" "medium" or "high"
- consent: "low" "medium" or "high"
- provenance: "low" "medium" or "high"
- platform_risk: "low" "medium" or "high"
- margin: "low" "medium" or "high"
- speed: "low" "medium" or "high"
- repeatability: "low" "medium" or "high"
- automation: "low" "medium" or "high"
- defensibility: "low" "medium" or "high"
- notes: optional context
returns decision plus rationale and next actions
usage:
~~~json
{
    "thoughts": [
        "I should screen this revenue lane before planning execution."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Opt-in inbox-to-CRM service for small businesses",
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "platform_risk": "medium",
        "margin": "medium",
        "speed": "medium",
        "repeatability": "high",
        "automation": "high",
        "defensibility": "medium",
        "notes": "Use client-owned inboxes and documented consent only."
    }
}
~~~
