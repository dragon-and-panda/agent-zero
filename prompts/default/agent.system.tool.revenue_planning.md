### revenue_planning

screen monetization ideas before execution
use for revenue strategies, venture prioritization, go-to-market planning, or when legality / consent / provenance need a fast policy check
reject personal-data resale, inbox scraping, non-consensual outreach, and other blocked lanes
prefer compliant reframes such as first-party workflow automation, opt-in funnels, public-data research products, and listing services
arguments:
- mission: short description of the monetization concept
- assets: optional description of data, tools, audience, or distribution already available
- constraints: optional legal, budget, staffing, or timeline constraints

returns:
- decision: PASS / HOLD / REJECT
- metrics: scored dimensions for legality, consent, TOS fit, speed, margin, repeatability, automation, defensibility, and reputation risk
- recommended_lanes: compliant lanes to pursue
- next_steps: concrete next actions

usage:
~~~json
{
    "thoughts": [
        "I should screen this monetization idea before building workflows around it."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "mission": "Build an agentic service that turns seller photos and notes into marketplace listings and manages inbound buyer messages.",
        "assets": "Agent Zero framework, listing blueprint, web UI, optional human approval for edge cases",
        "constraints": "Must avoid privacy abuse, spam, and platform evasion"
    }
}
~~~
