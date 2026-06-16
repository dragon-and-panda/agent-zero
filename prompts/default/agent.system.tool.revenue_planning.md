### revenue_planning:

Evaluates a revenue or growth plan for legality consent data provenance and platform risk before execution.

Use it before:
- data extraction from inboxes files or CRMs
- lead generation or outreach automation
- monetization plans involving marketplaces affiliate programs or services
- any request to buy sell rent enrich or broker contact data

Safety constraints:
- Reject inbox scraping personal-data resale unsolicited bulk outreach and plans that lack clear user authorization or recipient consent.
- Prefer first-party opt-in audiences documented business relationships compliant CRM hygiene and durable offers.
- When the plan is ambiguous the tool should hold execution and ask for missing compliance facts instead of assuming permission.

Arguments:
- `mission` (string, required): short description of the revenue or data workflow
- `data_sources` (string, optional): where the data would come from
- `consent_basis` (string, optional): opt-in contract existing customer relationship or other lawful basis
- `monetization_target` (string, optional): how the user plans to make money
- `notes` (string, optional): extra details or constraints

Usage:
```json
{
  "thoughts": ["I should assess whether this monetization workflow is compliant before I help implement it."],
  "tool_name": "revenue_planning",
  "tool_args": {
    "mission": "Clean and segment a first-party newsletter list for sponsored offers.",
    "data_sources": "Client-owned CRM export with opt-in timestamps.",
    "consent_basis": "Explicit newsletter opt-in with unsubscribe history.",
    "monetization_target": "Sponsored placements in the newsletter.",
    "notes": "Need guidance on safeguards and next steps."
  }
}
```
