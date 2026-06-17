### revenue_planning:
screen a proposed monetization lane before execution
use when the task involves business models, offers, growth systems, or revenue ideas
never use it to justify prohibited data extraction or contact-list resale

required inputs:
- lane: short descriptive name
- summary: what the lane does and who it serves
- legality: low|medium|high
- consent: low|medium|high
- provenance: low|medium|high
- platform_fit: low|medium|high
- time_to_cash: low|medium|high
- margin: low|medium|high
- repeatability: low|medium|high
- automation_fit: low|medium|high
- defensibility: low|medium|high

output:
- APPROVE if all hard gates clear and execution fit is strong
- HOLD if the lane may be lawful but needs validation or economics work
- REJECT if legality, consent, provenance, or platform fit are weak

example usage:
~~~json
{
    "thoughts": [
        "I should screen this revenue idea before trying to implement it.",
        "The lane needs a structured legality and viability check."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "lane": "Opt-in inbox-to-CRM assistant",
        "summary": "Turns a client's own opted-in inbound business email into CRM-ready records and drafts.",
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "platform_fit": "high",
        "time_to_cash": "medium",
        "margin": "medium",
        "repeatability": "high",
        "automation_fit": "high",
        "defensibility": "medium"
    }
}
~~~
