# Problem
Score a proposed revenue opportunity before spending build effort on it.

# Solution
1. Gather a short idea name plus 1-5 ratings for:
   - legality
   - consent
   - automation fit
   - margin potential
   - speed to first value
   - platform dependence
   - operational risk
2. Run:
   `bash /workspace/instruments/strategy/score.sh "<name>" <legality> <consent> <automation> <margin> <speed> <dependence> <risk>`
3. Read the output:
   - `GO` means the idea is suitable for immediate execution planning.
   - `HOLD` means the idea may be viable later but needs more derisking.
   - `REJECT` means the idea fails compliance or quality thresholds.
