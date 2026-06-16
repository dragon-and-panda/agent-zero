### revenue_planning:

screen a revenue idea before execution
use it when a task involves monetization lead generation data acquisition outreach or scaling an autonomous business workflow

purpose:
- reject illegal or non-consensual monetization plans early
- hold plans that need clearer consent provenance or terms review
- pass only plans that are lawful first-party and operationally attractive

arguments:
- mission: short summary of the business idea or workflow
- assets: what the agent already controls or can lawfully use
- data_sources: where data would come from
- acquisition_plan: how customers, leads, or data would be acquired
- monetization_plan: how money would be made
- delivery_plan: how value would be delivered
- constraints_json: optional JSON with explicit ratings or facts

constraints_json can include:
- authorized_access
- consent_status
- personal_data_resale
- tos_conflict
- legality
- consent
- provenance
- tos
- time
- margin
- repeatability
- automation
- defensibility

use before building workflows that touch inboxes gmail exports contact data scraping or outbound campaigns

usage:
```json
{
  "thoughts": [
    "This mission involves monetization and contact data, so I should screen it first."
  ],
  "tool_name": "revenue_planning",
  "tool_args": {
    "mission": "Use opted-in customer conversations to enrich a first-party CRM and sell a premium research subscription.",
    "assets": "Existing customer relationships, support inbox exports, product usage notes.",
    "data_sources": "Customer-owned inbox exports and consented CRM records.",
    "acquisition_plan": "Offer a lead magnet and collect explicit opt-in.",
    "monetization_plan": "Monthly subscription for benchmark reports.",
    "delivery_plan": "Automated report generation and a member portal."
  }
}
```
