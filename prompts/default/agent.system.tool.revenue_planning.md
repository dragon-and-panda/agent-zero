### revenue_planning:
screen and structure a monetization lane before execution

use this tool when asked to build revenue systems, evaluate ventures, or choose between monetization options

hard rule:
- reject any plan that depends on scraping, brokering, or selling personal email lists
- reject any plan with unclear consent, unclear data provenance, or terms-of-service conflicts

inputs:
- lane_name: short lane name
- summary: brief description of the revenue objective
- data_sources: describe what data would be used and who owns it
- hard_gates_json: JSON object with legality, consent, provenance, tos values
- soft_gates_json: JSON object with time, margin, repeatability, automation, defensibility values
- notes: optional rationale or pricing notes

outputs:
- decision: approve, hold, or reject
- rationale: concise decision summary
- safe_alternatives: replacement lanes if the original idea is not allowed
- policy_hits: any prohibited patterns that were detected

usage:
~~~json
{
    "thoughts": [
        "I should screen this monetization lane before executing anything."
    ],
    "tool_name": "revenue_planning",
    "tool_args": {
        "lane_name": "inbox_to_crm",
        "summary": "Turn a client-owned Gmail inbox into a CRM cleanup and follow-up service",
        "data_sources": "client-authorized Gmail export and CRM records",
        "hard_gates_json": "{\"legality\":\"pass\",\"consent\":\"pass\",\"provenance\":\"pass\",\"tos\":\"pass\"}",
        "soft_gates_json": "{\"time\":\"strong\",\"margin\":\"strong\",\"repeatability\":\"strong\",\"automation\":\"strong\",\"defensibility\":\"medium\"}",
        "notes": "monthly managed service"
    }
}
~~~
