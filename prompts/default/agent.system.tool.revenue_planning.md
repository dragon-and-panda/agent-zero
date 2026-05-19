### revenue_planning:
evaluate a proposed revenue workflow before execution
use for monetization ideas touching private data, outreach, marketplaces, or automation
rejects personal-data resale, unauthorized inbox/file extraction, and list brokerage
returns pass hold reject with reasons, controls, next actions, and safer alternatives
usage:
~~~json
{
    "thoughts": [
        "I should evaluate this venture before acting on it.",
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "objective": "Turn an owner-authorized support inbox into weekly operating summaries",
        "customer_value": "Saves operators time and highlights urgent follow-ups",
        "acquisition_model": "Direct sales to teams that own the mailbox",
        "monetization_model": "Monthly subscription",
        "data_source": "Customer-owned Gmail mailbox",
        "owner_authorized": true,
        "has_explicit_consent": false,
        "personal_data_involved": true,
        "value_strength": "high",
        "execution_feasibility": "medium",
        "repeatability": "medium",
        "legal_risk": "low",
        "consent_risk": "medium",
        "data_provenance_risk": "low",
        "platform_risk": "medium"
    }
}
~~~
