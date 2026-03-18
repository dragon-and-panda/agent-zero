# Problem
Classify an opportunity as GO, HOLD, or REJECT before work starts.

# Solution
1. Summarize the opportunity in one sentence.
2. Run `bash /workspace/instruments/strategy/score.sh "<summary>"`.
3. Use the result to update `docs/strategy/incoming.md`.
4. If the score is HOLD or REJECT, do not start execution until the blocking issue is removed.
