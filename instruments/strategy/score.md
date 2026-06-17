# Problem
Evaluate a proposed revenue lane or mission against legality, consent,
time-to-cash, automation fit, margin, and durability.

# Solution
1. Collect the lane name plus six 0-10 scores:
   - legality
   - consent
   - time_to_cash
   - automation_fit
   - margin
   - durability
2. Run the instrument:

```bash
bash /a0/instruments/strategy/score.sh "<lane-name>" <legality> <consent> <time_to_cash> <automation_fit> <margin> <durability>
```

3. Read the classification:
   - `GO` for compliant lanes ready to activate
   - `HOLD` for lanes needing more evidence or controls
   - `REJECT` for illegal, unethical, or non-consensual lanes
4. Save the result in the relevant mission journal before proceeding.

# Notes
- `legality` and `consent` are hard gates. Low scores on either field force a
  rejection even if the commercial scores are high.
- Start with service lanes that are client-owned, auditable, and fast to test.
