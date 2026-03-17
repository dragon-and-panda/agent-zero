# Problem
Rank candidate ventures for the autonomous revenue program.

# Solution
1. Create a CSV with these headers:
   `opportunity,legality,time_to_cash,automation_fit,margin,repeatability,downside_safety`
2. Run the instrument:
   - In Agent Zero runtime: `bash /a0/instruments/strategy/score.sh /path/to/opportunities.csv`
   - In this repo checkout: `bash instruments/strategy/score.sh /workspace/path/to/opportunities.csv`
3. Review the weighted score and decision (`GO`, `HOLD`, `REJECT`).

# Notes
- Scores should be 1-10.
- Any opportunity with `legality < 7` or `downside_safety < 5` is automatically rejected.
- Default weighting emphasizes legality and speed to cash over speculative upside.
