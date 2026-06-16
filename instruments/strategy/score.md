# Problem
Score a revenue lane before activating it.

# Solution
1. Run `bash /a0/instruments/strategy/score.sh` with these positional args:
   - legality: `low|medium|high`
   - consent: `low|medium|high`
   - provenance: `low|medium|high`
   - platform_rules: `low|medium|high`
   - time_to_cash: `low|medium|high`
   - margin: `low|medium|high`
   - repeatability: `low|medium|high`
   - automation_fit: `low|medium|high`
   - defensibility: `low|medium|high`
2. Read the output:
   - `REJECT` means the lane violates a hard gate and must not be pursued.
   - `HOLD` means the lane is allowed in principle but is not yet attractive enough to automate.
   - `PASS` means the lane is compliant and operationally viable enough to advance.
3. Save the score summary to program notes or memory before activating the lane.
