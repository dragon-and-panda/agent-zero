### revenue_planning:
screen a monetization idea before execution
use it when a task involves revenue strategy, data monetization, contact extraction, outreach lanes, or ambiguous legality
return PASS HOLD or REJECT with reasons and safer alternatives
usage:
~~~json
{
    "thoughts": [
        "I should screen this lane before building it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build a recurring revenue system from first-party customer operations.",
        "data_sources": "Owner-authorized customer export and support mailbox export.",
        "monetization": "CRM hygiene service for the customer, no resale.",
        "delivery": "Deduplicate contacts, summarize threads, sync tags into CRM.",
        "constraints": "Must stay lawful, consent-based, and platform-compliant."
    }
}
~~~
