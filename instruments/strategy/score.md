 # Strategy opportunity score

 Use `score.sh` to classify an opportunity as PASS, HOLD, or REJECT.

 Inputs are positional and use `low`, `medium`, or `high`:

 1. legality
 2. consent
 3. provenance
 4. tos_fit
 5. time_to_cash
 6. margin
 7. repeatability
 8. automation_fit
 9. defensibility

 Hard gates:
 - legality must not be low
 - consent must not be low
 - provenance must not be low
 - tos_fit must not be low

 Outcome rules:
 - REJECT if any hard gate is low
 - PASS if all hard gates clear and none of the execution factors are low
 - HOLD otherwise

 Examples:

 ```bash
 /workspace/instruments/strategy/score.sh high high high high high medium high high medium
 /workspace/instruments/strategy/score.sh high high high high medium low high medium medium
 /workspace/instruments/strategy/score.sh high low high high high high high high high
 ```
