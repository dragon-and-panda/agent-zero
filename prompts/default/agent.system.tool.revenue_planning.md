### revenue_planning:
screen a monetization idea before execution
use it for business model, acquisition, consent, provenance, or pricing decisions
reject personal-data resale, inbox scraping, spam-first outreach, or unclear provenance
prefer first-party, client-owned, and opt-in revenue lanes
important args:
- opportunity: concise lane summary
- customer: who pays
- offer: what is sold
- acquisition: how demand is generated
- data_provenance: first-party client-owned public-nonpersonal synthetic or risky source
- consent_model: yes or no
- legal: yes or no
- platform_terms: yes or no
- delivery: yes or no
- time_to_cash margin repeatability automation_fit defensibility: high medium or low
usage:
~~~json
{
    "thoughts": [
        "I should score this lane before acting on it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "opportunity": "Inbox-to-CRM assistant for founder mailboxes",
        "customer": "Founders and small teams",
        "offer": "Triage inboxes into tasks, CRM updates, and reply drafts",
        "acquisition": "Founder referrals and opt-in inbound demos",
        "data_provenance": "client-owned",
        "consent_model": "yes",
        "legal": "yes",
        "platform_terms": "yes",
        "delivery": "yes",
        "time_to_cash": "high",
        "margin": "medium",
        "repeatability": "high",
        "automation_fit": "high",
        "defensibility": "medium"
    }
}
~~~
