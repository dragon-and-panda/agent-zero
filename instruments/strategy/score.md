# Problem
Score a proposed revenue lane before activation.

# Solution
Run:

`bash /workspace/instruments/strategy/score.sh <legality> <consent> <provenance> <platform> <time_to_cash> <margin> <repeatability> <automation> <defensibility>`

Each input must be one of:

- `low`
- `medium`
- `high`

Interpretation:

- `REJECT`: a hard gate failed
- `HOLD`: compliant enough to explore, but unattractive or under-specified
- `PASS`: compliant and operationally promising
