### revenue_planning:

Screen a monetization or venture idea before execution.

Use it when the task involves:

- choosing between revenue lanes
- checking legality, consent, provenance, or platform fit
- redirecting unsafe monetization ideas into compliant alternatives
- evaluating whether an autonomous business workflow should be activated now

Primary args:

- `idea`: short description of the lane or proposal
- `target_customer`: who pays
- `assets`: relevant assets already owned
- `data_sources`: where the data comes from
- `acquisition_method`: how customers or data are acquired
- `monetization_model`: subscription, service, software, internal ops, etc.
- `execution_notes`: extra constraints or rollout notes
- `ratings_json`: optional JSON object with manual factor overrides using `low`, `medium`, or `high`

The tool returns a structured decision: `REJECT`, `HOLD`, or `PASS`, plus reasons, safer alternatives, and next actions.

Example:
```json
{
  "tool_name": "revenue_planning",
  "tool_args": {
    "idea": "Use an authorized business inbox to extract inbound leads into a CRM",
    "target_customer": "Our own sales team",
    "data_sources": "first-party authorized mailbox data",
    "acquisition_method": "inbound and opt-in",
    "monetization_model": "internal revenue operations automation"
  }
}
```
