# Problem
Score a proposed revenue lane before activation.

# Solution
1. Rate the idea from 0 to 10 on each input:
   - legality
   - consent
   - data_rights
   - time_to_cash
   - automation_fit
   - unit_economics
2. Run:
   `bash /a0/instruments/strategy/score.sh <legality> <consent> <data_rights> <time_to_cash> <automation_fit> <unit_economics>`
3. Use the output:
   - `REJECT` if legality, consent, or data-rights confidence is weak
   - `HOLD` if the idea is lawful but the economics or execution profile are not yet strong
   - `GO` if the weighted score is strong and all hard gates pass

## Example

`bash /a0/instruments/strategy/score.sh 10 10 9 7 8 8`
