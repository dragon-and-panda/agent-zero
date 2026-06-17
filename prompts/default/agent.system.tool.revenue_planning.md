### revenue_planning:
screen a revenue idea before executing monetization or data-acquisition work
use for business models, lead generation, outreach plans, crm extraction, or autonomous revenue lanes
returns PASS HOLD or REJECT with hard gates soft scores safer alternatives and next steps
rejects private-data resale inbox scraping spam and other non-consensual workflows

**Example usage**:
~~~json
{
    "thoughts": [
        "I should screen this monetization plan before taking action."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build an inbox-to-CRM service for a consenting mailbox owner",
        "data_sources": "Owner-authorized Gmail mailbox and customer-owned CRM",
        "acquisition_method": "First-party automation",
        "offer": "CRM cleanup and follow-up workflow",
        "monetization": "Monthly retainer"
    }
}
~~~
