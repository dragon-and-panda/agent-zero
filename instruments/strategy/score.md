# Strategy scoring instrument

Use this instrument to evaluate proposed ventures and revenue lanes before execution.

## Purpose
- reject illegal, privacy-invasive, or platform-abusive ideas early
- hold compliant ideas that are too weak operationally
- pass only ideas that are compliant and commercially credible

## Inputs
Run `./instruments/strategy/score.sh` with 10 positional arguments:

1. legality: `low|medium|high`
2. consent: `low|medium|high`
3. provenance: `low|medium|high`
4. platform_risk: `low|medium|high` where `high` means low practical risk because the lane is compatible with platform rules
5. time_to_cash: `low|medium|high`
6. margin: `low|medium|high`
7. repeatability: `low|medium|high`
8. automation_fit: `low|medium|high`
9. defensibility: `low|medium|high`
10. reversibility: `low|medium|high`

## Decision policy
- `REJECT` if legality is not high
- `REJECT` if consent is not high
- `REJECT` if provenance is not high
- `REJECT` if platform compatibility or reversibility is low
- `HOLD` if any soft execution factor is low
- `PASS` only if at least three soft execution factors are high, none are low, and platform compatibility is high

## Example outcomes
```bash
# PASS: compliant and commercially attractive
./instruments/strategy/score.sh \
  high high high high \
  medium high high high medium high

# HOLD: compliant, but weak repeatability
./instruments/strategy/score.sh \
  high high high high \
  medium high low high medium high

# REJECT: unclear consent
./instruments/strategy/score.sh \
  high medium high high \
  high high high high high high
```
