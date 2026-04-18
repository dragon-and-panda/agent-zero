# Problem
Screen a monetization idea before building it.

# Solution
1. Rate the opportunity on each dimension using `low`, `medium`, or `high`.
2. Run:
   `bash /a0/instruments/strategy/score.sh <legality> <consent> <provenance> <tos> <margin> <repeatability> <automation> <defensibility> <time_to_cash> <setup_complexity>`
3. Read the verdict:
   - `PASS` means the lane is compliant and commercially attractive enough to prioritize.
   - `HOLD` means the lane is not rejected, but needs diligence or has weak economics.
   - `REJECT` means the idea fails a hard compliance gate and should not proceed.

# Notes
- Hard gates are legality, consent, provenance, and platform compatibility.
- Low setup complexity is better, so the script internally flips that factor into an execution score.
- Do not treat a `HOLD` as approval. It means gather evidence or improve the lane first.
