### revenue_planning:

Review a revenue idea against legality, consent, provenance, and platform-risk gates.
Use this before executing monetization workflows that touch customer data, inboxes, contact records, outreach, or marketplace automation.

The tool returns a JSON plan with:

- `verdict`: `PASS`, `HOLD`, or `REJECT`
- `reasons`: why the idea is blocked or acceptable
- `required_controls`: what must be clarified before execution
- `recommended_alternatives`: safer business models when the idea is not acceptable

Arguments:

- `objective`: one-sentence description of the venture or workflow
- `revenue_model`: how money would be made
- `data_source`: where the inputs would come from
- `owner_authorized`: whether the operator owns or is explicitly authorized to use the data
- `consent_status`: `explicit`, `contractual`, `internal`, `unknown`, or `none`
- `data_provenance`: `first_party`, `licensed`, `opt_in`, `public`, `scraped`, `purchased`, or `unknown`
- `platform_risk`: `low`, `medium`, or `high`
- `notes`: optional extra context

Usage:
```json
{
  "thoughts": [
    "This revenue idea touches contact data, so I should run a compliance-first planning pass."
  ],
  "tool_name": "revenue_planning",
  "tool_args": {
    "objective": "Clean and segment a founder's opt-in newsletter list",
    "revenue_model": "productized service",
    "data_source": "owner-authorized first-party export",
    "owner_authorized": true,
    "consent_status": "explicit",
    "data_provenance": "first_party",
    "platform_risk": "low"
  }
}
```
