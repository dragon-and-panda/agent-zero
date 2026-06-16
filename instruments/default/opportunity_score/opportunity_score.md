# Problem
Rank possible revenue opportunities without drifting into low-consent or legally risky tactics.

# Solution
1. Prepare a JSON file describing one or more opportunities.
2. Run:
   `python3 /a0/instruments/default/opportunity_score/opportunity_score.py <path-to-json>`
3. Review the ranked output and reject any opportunity marked `REJECT`.
4. Use `--example` to print a starter JSON payload.

# Expected JSON shape
```json
[
  {
    "name": "Inbox-to-offer audit",
    "consent_strength": 5,
    "legality_safety": 5,
    "automation_fit": 4,
    "time_to_revenue": 4,
    "margin_potential": 4,
    "repeatability": 4,
    "strategic_fit": 5,
    "startup_cost": 2,
    "notes": "Uses owned inbox exports and a fixed-scope audit."
  }
]
```

# Scoring notes
- All numeric fields use a `0-5` scale.
- Higher is better for every field except `startup_cost`, where lower cost helps the score.
- Opportunities with weak consent or legality are marked `REJECT` even if the raw score is high.
