### revenue_planning:

screen a revenue lane for legality consent tos fit and operational quality

use this before pursuing monetization ideas or data workflows
especially when the task involves inbox data contact data scraping outreach brokerage marketplaces or autonomous selling

returns:
- status: PASS HOLD or REJECT
- summary: short recommendation
- reasoning: factor breakdown
- safer_alternative: compliant replacement lane when needed

example:
~~~json
{
    "thoughts": [
        "Need to evaluate the revenue idea before acting",
        "This tool can score legality consent and repeatability",
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "lane_name": "Owner-authorized inbox to CRM cleanup service",
        "description": "Connect a business Gmail inbox, classify inbound leads, and sync only opted-in records into the company's CRM.",
        "inputs": "authorized mailbox access, CRM account, consent fields, business rules",
        "data_sources": "customer inbox, website forms, CRM",
        "delivery_model": "managed service",
        "monetization_model": "monthly retainer",
        "automation_level": "high",
        "legal_basis": "company-owned inbox with explicit authorization and consented lead handling",
        "consent_model": "first-party consent",
        "tos_risk": "low"
    }
}
~~~
