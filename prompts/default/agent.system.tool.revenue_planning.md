### revenue_planning

Use this before acting on missions involving monetization, outreach, inboxes, contacts, CRM data, or list building.

It classifies the plan as:

- PASS: compliant and suitable to execute
- HOLD: possible, but requires explicit ownership, consent, provenance, or platform controls
- REJECT: illegal, privacy-invasive, spam-like, or disallowed

Prefer this tool whenever the request mentions:

- revenue generation
- lead generation
- Gmail or inbox processing
- email address extraction
- audience building
- selling data or lists

usage:

~~~json
{
    "thoughts": [
        "I should classify this revenue workflow before touching data or outreach."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build a profitable workflow from a client's support inbox.",
        "context": "Need to use only owner-authorized and consent-compatible data."
    }
}
~~~
