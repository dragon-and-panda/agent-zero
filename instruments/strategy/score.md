# Problem
Score a revenue idea against legality, consent, data rights, and platform risk.

# Solution
1. Use only `low`, `medium`, or `high` for each input.
2. Run:
   `bash /a0/instruments/strategy/score.sh <legality_confidence> <consent_strength> <data_rights_confidence> <platform_risk>`
3. Treat the output as a gating decision:
   - `PASS` means the idea can move into planning
   - `HOLD` means gather more evidence or add controls before planning
   - `REJECT` means do not implement the idea

# Examples
- `bash /a0/instruments/strategy/score.sh high high high low` -> PASS
- `bash /a0/instruments/strategy/score.sh high medium high low` -> HOLD
- `bash /a0/instruments/strategy/score.sh low low low high` -> REJECT
