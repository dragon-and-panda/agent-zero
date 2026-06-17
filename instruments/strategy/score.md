# Problem
Decide whether a revenue opportunity should be activated, held, or rejected.

# Solution
Run the strategy scoring instrument with six 0-10 inputs:

1. legality
2. consent
3. time_to_cash
4. automation_leverage
5. margin_potential
6. defensibility

Usage:
`bash /a0/instruments/strategy/score.sh <legality> <consent> <time_to_cash> <automation_leverage> <margin_potential> <defensibility>`

Notes:
- legality and consent are hard gates; low values force REJECT.
- the tool prints the weighted score and a GO/HOLD/REJECT recommendation.
- use this before building a new monetization lane.
