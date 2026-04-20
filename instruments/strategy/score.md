# Strategy Scoring Instrument

This instrument evaluates a proposed revenue lane before activation.

Output one of:

- PASS: strong candidate, compliant, attractive, ready for controlled execution
- HOLD: compliant or partially compliant, but unclear, weak, or not yet attractive
- REJECT: fails hard gates or depends on prohibited behavior

Hard gates:

1. legality
2. consent
3. provenance
4. tos

Soft factors:

1. time
2. margin
3. repeatability
4. automation
5. defensibility

Input scale:

- `high`: clearly favorable
- `medium`: acceptable but not strong enough to auto-activate
- `low`: weak or unsafe

Rules:

- If any hard gate is `low`, result is REJECT.
- If any soft factor is `low`, result is HOLD unless already REJECT.
- PASS requires:
  - all hard gates are `high`
  - no soft factor is `low`
  - at least three soft factors are `high`
- Otherwise return HOLD.

Suggested invocation:

```bash
./instruments/strategy/score.sh \
  "lane=Inbox to CRM copilot" \
  "legality=high" \
  "consent=high" \
  "provenance=high" \
  "tos=high" \
  "time=medium" \
  "margin=high" \
  "repeatability=high" \
  "automation=high" \
  "defensibility=medium"
```
