# Problem
Score a proposed revenue opportunity before committing time or automation effort.

# Solution
1. Choose 1-5 ratings for the opportunity across these factors:
   - legality
   - privacy
   - time_to_cash
   - automation_fit
   - demand
   - durability
2. Run:
   `bash /workspace/instruments/strategy/score.sh "<name>" <legality> <privacy> <time_to_cash> <automation_fit> <demand> <durability>`
3. Treat the result as:
   - `GO` when the opportunity is compliant and attractive enough to start,
   - `HOLD` when it is potentially viable but not ready,
   - `REJECT` when legality or privacy is weak.

# Notes
- Any legality or privacy score below 4 should be treated as a stop sign.
- Use this instrument before adding work to the active execution queue.
