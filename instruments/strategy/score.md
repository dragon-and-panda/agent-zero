# Problem
Rank a proposed revenue lane before launching autonomous work.

# Solution
1. Write a short description of the lane you want to evaluate.
2. Run:
   `bash /a0/instruments/strategy/score.sh "<lane name>" <legality> <consent> <time_to_cash> <automation_fit> <complexity> <defensibility>`
3. Use 1-10 scores for each factor.
4. Reject the lane if the script reports `REJECT`.

# Notes
- `legality` and `consent` are hard gates.
- `complexity` is inverted inside the scoring model; lower complexity helps.
- The instrument is meant to prevent unsafe or low-trust monetization ideas from consuming agent time.

# Example
`bash /a0/instruments/strategy/score.sh "Inbox-to-CRM automation" 9 10 8 9 4 7`
