# Problem
Score a potential revenue opportunity before the agency commits time, money, or data access.

# Solution
1. Use the scoring instrument:
   - `bash /a0/instruments/strategy/score.sh opportunity="Inbox-to-CRM Hygiene Service" legality=5 consent=5 time_to_cash=4 margin=4 automation_fit=5 defensibility=3 data_sensitivity=1 delivery_risk=2 reputation_risk=1 capital_required=1`
2. Review the verdict:
   - `GO` = proceed to offer design or pilot
   - `HOLD` = improve the plan first
   - `REJECT` = do not pursue in current form

# Scoring Rules
- `legality` and `consent` below `4` force `REJECT`
- `data_sensitivity` above `2` forces `REJECT`
- `reputation_risk` above `3` forces `REJECT`
- Higher scores are better for:
  - `legality`
  - `consent`
  - `time_to_cash`
  - `margin`
  - `automation_fit`
  - `defensibility`
- Lower scores are better for:
  - `data_sensitivity`
  - `delivery_risk`
  - `reputation_risk`
  - `capital_required`

# Suggested Scale
- `1` = poor / high risk / slow
- `3` = acceptable but mixed
- `5` = strong / low risk / fast
