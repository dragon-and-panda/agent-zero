# Strategy Scoring Instrument

This instrument screens new revenue lanes before activation.

## Inputs

Run `instruments/strategy/score.sh` with these ordered arguments:

1. legality: `low|medium|high`
2. consent: `low|medium|high`
3. provenance: `low|medium|high`
4. platform risk: `low|medium|high`
5. time-to-cash: `low|medium|high`
6. margin quality: `low|medium|high`
7. repeatability: `low|medium|high`
8. automation fit: `low|medium|high`
9. defensibility: `low|medium|high`

## Hard gates

Reject immediately if:

- legality is not `high`
- consent is not `high`
- provenance is not `high`
- platform risk is `high`

## Soft evaluation

Among the five execution factors:

- time-to-cash
- margin quality
- repeatability
- automation fit
- defensibility

Return:

- `PASS` when no factor is `low` and at least three are `high`
- `HOLD` when the lane is compliant but not yet attractive enough to activate
- `REJECT` when a hard gate fails

## Example

```bash
./instruments/strategy/score.sh high high high low high medium high high medium
```
