# Strategy Score Instrument

`score.sh` provides a lightweight triage for new revenue lanes.

## Inputs

Hard gates:
- `legality`: `low|medium|high`
- `consent`: `low|medium|high`
- `provenance`: `low|medium|high`
- `platform_risk`: `low|medium|high`

Soft execution factors:
- `time`: `low|medium|high`
- `margin`: `low|medium|high`
- `repeatability`: `low|medium|high`
- `automation`: `low|medium|high`
- `defensibility`: `low|medium|high`

Interpretation:
- for `legality`, `consent`, and `provenance`, `high` is best
- for `platform_risk`, `low` is best
- for the soft factors, `high` is best

## Outcomes

- `REJECT`: any hard gate fails
- `HOLD`: hard gates clear, but the economics or automation profile are weak
- `PASS`: hard gates clear, no soft factor is low, and at least three soft
  factors are high

## Example

```bash
instruments/strategy/score.sh   legality=high consent=high provenance=high platform_risk=low   time=medium margin=high repeatability=high automation=high defensibility=medium
```
