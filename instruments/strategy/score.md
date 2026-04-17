# Problem

Score a proposed venture lane before execution.

# Solution

1. Rate the lane using `low`, `medium`, or `high` for each factor:
   - legality
   - consent
   - provenance
   - tos_fit
   - margin
   - automation
   - repeatability
   - defensibility
   - time_to_cash
2. Run:
   `bash /a0/instruments/strategy/score.sh <legality> <consent> <provenance> <tos_fit> <margin> <automation> <repeatability> <defensibility> <time_to_cash>`
3. Read the result:
   - `REJECT` means do not pursue the lane
   - `HOLD` means the lane is compliant enough to revisit later but weak for current focus
   - `PASS` means the lane clears hard gates and is commercially attractive enough to prioritize
