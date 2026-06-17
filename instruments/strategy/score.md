# Problem
Score a candidate revenue lane before activating it.

# Solution
1. Evaluate the lane on these hard gates: `legality`, `consent`, `provenance`, `tos`.
2. Evaluate these soft factors: `time`, `margin`, `repeatability`, `automation`, `defensibility`.
3. Run:

   `bash /a0/instruments/strategy/score.sh <legality> <consent> <provenance> <tos> <time> <margin> <repeatability> <automation> <defensibility>`

4. Use only `low`, `medium`, or `high` for each input.
5. Interpret the result:
   - `REJECT`: one or more hard gates failed.
   - `HOLD`: hard gates passed, but the lane is still weak or immature.
   - `PASS`: hard gates passed and the lane is strong enough to run now.

# Examples
- `bash /a0/instruments/strategy/score.sh high high high high medium high high high medium`
- `bash /a0/instruments/strategy/score.sh high high high high low medium medium medium medium`
- `bash /a0/instruments/strategy/score.sh high medium high high high high high high high`
