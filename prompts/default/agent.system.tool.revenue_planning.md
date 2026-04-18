### revenue_planning:
screen a monetization idea for legality privacy consent and execution quality
usage:
~~~json
{
    "thoughts": [
        "I should screen this revenue idea before activating it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "idea": "Offer an opt-in inbox cleanup and CRM setup service for small businesses.",
        "customer": "small businesses",
        "value_proposition": "convert messy inbound email into a tagged CRM pipeline",
        "delivery_model": "service",
        "data_sources": "client-provided inbox exports, voluntary CRM records",
        "channels": "direct outreach to existing network, website, referrals",
        "consent_basis": "written client authorization and first-party data only",
        "platform_dependencies": "gmail api, hubspot, notion",
        "time_to_cash": "medium",
        "margin": "high",
        "repeatability": "medium",
        "automation_potential": "high",
        "defensibility": "medium"
    }
}
~~~

returns:
- status: PASS, HOLD, or REJECT
- hard_gates: legality, consent, provenance, platform compliance
- next_steps: compliant activation plan or reasons to stop
