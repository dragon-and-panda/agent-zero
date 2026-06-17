## Strategy score instrument

Purpose: screen a monetization lane before activation.

Hard gates:
- legality: yes or no
- consent: yes or no
- provenance: first_party, client_owned, licensed, public_nonpersonal, or unclear
- tos_ok: yes or no

Soft factors:
- time_to_cash: low, medium, high
- margin: low, medium, high
- repeatability: low, medium, high
- automation_fit: low, medium, high
- defensibility: low, medium, high

Decision logic:
- REJECT if legality is no, consent is no, tos_ok is no, or provenance is unclear.
- PASS only if all hard gates clear and every soft factor is medium or high with at least three highs.
- HOLD otherwise.

Example:
```bash
./instruments/strategy/score.sh \
  high high high low \
  medium high high high medium
```

The positional fields map to:
1. legality
2. consent
3. provenance
4. tos_conflict
5. time
6. margin
7. repeatability
8. automation
9. defensibility
