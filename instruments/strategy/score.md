# Problem
Score a business or automation idea before spending time building it.

# Solution
1. Gather six 0-10 ratings:
   - legality
   - consent
   - time_to_cash
   - defensibility
   - operational_fit
   - reputational_safety
2. Run:
   `bash /a0/instruments/strategy/score.sh <legality> <consent> <time_to_cash> <defensibility> <operational_fit> <reputational_safety>`
3. Interpret the result:
   - REJECT: do not pursue as proposed
   - HOLD: research or redesign before activation
   - GO: compliant enough to prototype, subject to normal validation

# Guidance
- If legality < 7, the idea is rejected automatically.
- If consent < 7, the idea is rejected automatically.
- If reputational_safety < 5, the idea is rejected automatically.
- Use conservative scoring when personal data, account access, scraping, or regulated industries are involved.
