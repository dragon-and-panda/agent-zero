# Problem
Score monetization opportunities quickly and consistently.

# Solution
1. Prepare a CSV with columns:
   - `name`
   - `market_demand` (0-10)
   - `margin_potential` (0-10)
   - `execution_speed` (0-10)
   - `compliance_risk` (0-10, where higher is worse)
   - `automation_fit` (0-10)
2. Run:
   - `bash /a0/instruments/custom/opportunity_score/opportunity_score.sh <input.csv> [output.csv]`
3. The script writes sorted opportunities by composite score and prints the top 5.

# Notes
- Compliance risk is negatively weighted.
- Use this before launching weekly monetization experiments.
