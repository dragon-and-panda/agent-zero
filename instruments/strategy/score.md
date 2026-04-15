# Problem
Score a proposed revenue lane before activation.

# Solution
1. Use this instrument only for opportunities that are already described in plain language.
2. Provide six scores from 0 to 10 in this order:
   - legality
   - consent
   - time_to_cash
   - margin
   - automation_fit
   - repeatability
3. Run:
   - `bash /a0/instruments/strategy/score.sh 10 10 8 7 9 8`
   - or `bash /a0/instruments/strategy/score.sh legality=10 consent=10 time_to_cash=8 margin=7 automation_fit=9 repeatability=8`
4. Respect the hard gates:
   - low legality rejects the lane
   - low consent rejects the lane
5. Treat the output as a decision aid:
   - GO means eligible to pilot
   - HOLD means refine or de-risk first
   - REJECT means do not activate
