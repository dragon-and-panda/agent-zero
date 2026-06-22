### revenue_strategy:

Create a legal and ethical monetization plan for an online venture or agent workflow.

Use it for:
- business-model selection
- opt-in lead generation plans
- affiliate, content, SaaS, or productized-service ideas
- automation workflows that still need compliance guardrails

Args:
- **venture**: short description of the venture or capability
- **market**: target niche or customer segment
- **goal**: revenue or growth objective
- **assets_json**: JSON object describing skills, assets, channels, budget, data you already own with permission
- **constraints_json**: JSON object for legal, ethical, brand, budget, or staffing constraints

This tool blocks tactics like selling harvested email lists, scraping private inboxes, or using spam as a growth channel.

usage:
```json
{
  "thoughts": ["I need a compliant go-to-market plan for a small autonomous business."],
  "tool_name": "revenue_strategy",
  "tool_args": {
    "venture": "AI workflow audits for small ecommerce teams",
    "market": "Shopify stores doing 50k-500k ARR",
    "goal": "Reach first 10 paying customers without paid ads",
    "assets_json": "{\"skills\":[\"Python\",\"automation\",\"copywriting\"],\"channels\":[\"blog\",\"LinkedIn\"],\"budget_usd\":500}",
    "constraints_json": "{\"must_be_opt_in\":true,\"no_personal_data_resale\":true,\"region\":\"US/EU\"}"
  }
}
```
