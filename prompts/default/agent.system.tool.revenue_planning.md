### revenue_planning:

screen a monetization idea before execution

use this tool when a task involves revenue generation go-to-market lead generation outbound outreach data acquisition or any business model with legal privacy or platform-policy risk

hard gates:
- legality
- consent
- provenance
- platform_alignment

soft factors:
- time_to_cash
- margin
- repeatability
- automation
- defensibility

rating values must be low medium or high

rules:
- any hard gate low => reject
- any hard gate medium => hold until clarified or redesigned
- if hard gates are high but any soft factor is low => hold
- pass only when hard gates are high no soft factor is low and at least three soft factors are high
- reject immediately if the idea relies on personal-data resale inbox scraping contact-list brokerage spam or other unauthorized collection or use of personal data

usage:
~~~json
{
    "tool_name": "revenue_planning",
    "tool_args": {
        "lane_name": "Opt-in local business listing service",
        "summary": "Create and manage listings for small businesses that explicitly hire us.",
        "target_customer": "Local service businesses",
        "delivery_model": "Done-for-you service with recurring maintenance",
        "data_sources": "Client-provided details, public business info, first-party performance data",
        "acquisition_path": "Inbound content and referrals",
        "value_exchange": "Improved search visibility and lead capture",
        "consent_basis": "Client authorization and opt-in onboarding",
        "platform_dependencies": "Google Business Profile, Yelp, directories",
        "geography": "US",
        "legality": "high",
        "consent": "high",
        "provenance": "high",
        "platform_alignment": "high",
        "time_to_cash": "medium",
        "margin": "medium",
        "repeatability": "high",
        "automation": "high",
        "defensibility": "medium",
        "risk_notes": "Need SOPs for client onboarding and change approvals."
    }
}
~~~
