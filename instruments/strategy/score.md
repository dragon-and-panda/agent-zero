# Problem
Score a candidate revenue lane before activating it.

# Solution
1. Run `bash /a0/instruments/strategy/score.sh lane="<name>" legality=<0-5> consent=<0-5> automation=<0-5> time_to_cash=<0-5> redundancy=<0-5> capex=<0-5> market_access=<0-5> data_risk=<0-5>`
2. Read the `decision`, `score`, and `next_action` output.
3. Only activate lanes that return `decision=GO` and do not conflict with `docs/policies/compliance_pack.md`.

# Notes
- Higher `data_risk` is worse; all other fields are better when higher.
- Any lane with weak legality or consent should be rejected, even if the raw score is high.
