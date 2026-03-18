# Problem
Choose the best ethical revenue opportunity to launch next.

# Solution
1. Score each candidate offer before committing resources.
2. Run:

   `bash instruments/default/revenue_score/revenue_score.sh --name "<offer>" --impact <1-5> --time-to-cash <1-5> --automation-fit <1-5> --confidence <1-5> --redundancy <1-5> --setup-cost <1-5> --compliance-risk <1-5>`

3. Interpret the result:
   - `80-100`: launch now
   - `60-79`: incubate with constraints
   - `0-59`: hold or reject

## Scoring guidance
- `impact`: revenue and strategic upside
- `time-to-cash`: how quickly cash can be collected
- `automation-fit`: how well the workflow can be systematized
- `confidence`: confidence that buyers and delivery capacity exist
- `redundancy`: how much this offer improves channel diversification
- `setup-cost`: upfront cost and complexity, where `1` is low cost and `5` is high cost
- `compliance-risk`: legal/privacy/platform risk, where `1` is low risk and `5` is high risk
