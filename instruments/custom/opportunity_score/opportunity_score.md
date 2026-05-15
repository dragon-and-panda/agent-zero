# Problem
Score and rank venture ideas for ethical, autonomous revenue generation.

# Solution
1. Put your ideas in a JSON file.
2. Run:
   `bash /a0/instruments/custom/opportunity_score/opportunity_score.sh /a0/path/to/ideas.json`
3. Review the markdown report printed by the instrument.

# Input format
The JSON file may contain a single object, a list of objects, or an object with
an `ideas` array.

Each idea can include:

```json
{
  "name": "Autonomous listing concierge",
  "description": "Optimize seller listings and syndicate them across marketplaces.",
  "revenue_model": "service",
  "acquisition_model": "seo",
  "scores": {
    "demand": 8,
    "margin": 7,
    "automation": 8,
    "speed_to_revenue": 7,
    "recurring_revenue": 6,
    "defensibility": 6,
    "setup_complexity": 4,
    "compliance_risk": 2,
    "data_sensitivity": 2,
    "platform_dependency": 5
  }
}
```

# Notes
- Scores are 0 to 10.
- Higher is better for demand, margin, automation, speed to revenue,
  recurring revenue, and defensibility.
- Higher is worse for setup complexity, compliance risk, data sensitivity, and
  platform dependency.
- The instrument automatically flags risky concepts such as selling email lists,
  scraping inboxes without authority, or data brokerage.
