# Strategy Scoring Instrument

Use `/workspace/instruments/strategy/score.sh` to screen a proposed revenue lane before activation.

## Inputs

Provide one value for each factor:

- legality: `low|medium|high`
- consent: `low|medium|high`
- provenance: `low|medium|high`
- tos_conflict: `low|medium|high`
- time: `low|medium|high`
- margin: `low|medium|high`
- repeatability: `low|medium|high`
- automation: `low|medium|high`
- defensibility: `low|medium|high`

## Hard gates

The lane is an automatic `REJECT` if:

- legality is `low`
- consent is `low`
- provenance is `low`
- tos_conflict is `high`

If legality, consent, provenance, or platform clarity is only `medium`, the lane remains `HOLD` until the ambiguity is resolved.

## Outcome logic

- `PASS`: all hard gates clear, no soft execution factor is `low`, and at least three soft factors are `high`
- `HOLD`: compliant directionally, but one or more gates are only partial or the execution profile is weak
- `REJECT`: fails a hard gate or relies on strong platform conflict

## Example commands

```bash
bash /workspace/instruments/strategy/score.sh high high high low high high high high high
bash /workspace/instruments/strategy/score.sh high high high low medium medium high medium medium
bash /workspace/instruments/strategy/score.sh high low high low high high high high high
```
