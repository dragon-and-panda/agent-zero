# Problem
Score a business lane before investing agent time.

# Solution
Run:

`bash /a0/instruments/strategy/score.sh "<lane_name>" <legality> <consent> <time_to_cash> <defensibility> <autonomy_fit> <effort_efficiency>`

Inputs are six integers from 0 to 10:

1. legality
2. consent
3. time_to_cash
4. defensibility
5. autonomy_fit
6. effort_efficiency

Hard gates:

- legality < 7 -> REJECT
- consent < 7 -> REJECT

Weighted decision:

- GO if weighted score >= 7.5
- HOLD if weighted score >= 6.0 and < 7.5
- REJECT otherwise

Example:

`bash /a0/instruments/strategy/score.sh "Inbox-to-CRM Hygiene" 9 10 8 7 9 8`
