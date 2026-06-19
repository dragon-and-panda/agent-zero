### revenue_planning:
use before acting on monetization, outreach, inbox-data, lead-gen, or contact-data ideas
checks legality, consent, provenance, and platform risk
use it to reject unsafe ideas early and redirect to compliant revenue lanes
args:
- objective: goal or business idea
- data_sources: comma or newline list of data sources
- intended_actions: comma or newline list of planned actions
- constraints: extra constraints or assumptions
usage:
~~~json
{
    "thoughts": [
        "I should assess the monetization path before building it.",
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "objective": "Create a recurring-revenue service around client workflow automation",
        "data_sources": "client-owned CRM export, public docs",
        "intended_actions": "clean internal records, generate process recommendations",
        "constraints": "must stay compliant and low-touch"
    }
}
~~~
