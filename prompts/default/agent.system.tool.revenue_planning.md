### revenue_planning:
screen a revenue idea for legality, consent, provenance, platform risk, and execution attractiveness

Use this tool before activating any monetization lane, especially if the request touches email, outreach, scraped data, inbox content, marketplaces, payments, or regulated domains.

The tool returns:
- decision: PASS, HOLD, or REJECT
- scores: normalized factor ratings
- reasons: hard or soft reasons behind the decision
- recommended_next_step: compliant follow-up action

Example usage:
~~~json
{
    "thoughts": [
        "I should score this monetization idea before acting on it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "lane_name": "Inbox-to-CRM follow-up operator",
        "summary": "Use the owner's inbox to identify overdue invoices and create a consented CRM follow-up workflow.",
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "platform_risk": "low",
        "time": "medium",
        "margin": "medium",
        "repeatability": "high",
        "automation": "high",
        "defensibility": "medium"
    }
}
~~~
