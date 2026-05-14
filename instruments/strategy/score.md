# Strategy Score Instrument

Use this instrument to block obviously unsafe monetization ideas before implementation.

## Command

```bash
bash /workspace/instruments/strategy/score.sh <legality> <consent> <provenance> <platform_risk> <offer_clarity>
```

Every input must be one of:

- `low`
- `medium`
- `high`

## Meaning

- legality: confidence that the model is lawful and compliant
- consent: quality of end-user permission for any retained data or outreach
- provenance: how trustworthy and licensed the data source is
- platform_risk: chance the workflow violates platform or account terms
- offer_clarity: how concrete the paid offer is

## Examples

```bash
bash /workspace/instruments/strategy/score.sh high high high low high
# PASS

bash /workspace/instruments/strategy/score.sh medium medium high medium low
# HOLD

bash /workspace/instruments/strategy/score.sh high low high low high
# REJECT
```
