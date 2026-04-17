# Problem
Decide whether a proposed revenue lane is safe and worth activating.

# Solution
1. Run `bash /workspace/instruments/strategy/score.sh` with numeric scores from 0-5.
2. Required flags:
   - `--lane "<name>"`
   - `--legality N`
   - `--consent N`
   - `--tos N`
   - `--evidence N`
   - `--reserve N`
   - `--risk N`
   - `--time N`
   - `--margin N`
   - `--repeatability N`
   - `--automation N`
   - `--defensibility N`
3. The instrument returns one of:
   - `PASS` when hard gates clear and execution quality is strong,
   - `HOLD` when compliant but not yet attractive or proven,
   - `REJECT` when legality, consent, TOS, or risk gates fail.
4. Save the result in the relevant mission diary before activation.
