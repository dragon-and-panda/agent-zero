# Strategy Scoring Instrument

Use `/workspace/instruments/strategy/score.sh` to screen a proposed revenue lane before activation.

## Inputs

Provide one value for each factor:

- legality: `high|medium|low`
- consent: `high|medium|low`
- provenance: `high|medium|low`
- tos: `high|medium|low`
- time: `high|medium|low`
- margin: `high|medium|low`
- repeatability: `high|medium|low`
- automation: `high|medium|low`
- defensibility: `high|medium|low`

## Hard gates

The lane is an automatic `REJECT` if any of these are not `high`:

- legality
- consent
- provenance

The lane is also an automatic `REJECT` if platform or contractual fit (`tos`) is `low`.

## Outcome logic

- `PASS`: all hard gates clear and every soft factor is at least `medium`
- `HOLD`: compliant lane, but one or more soft factors are `low` or too many are only `medium`
- `REJECT`: fails a hard gate or platform-fit gate

## Example commands

```bash
bash /workspace/instruments/strategy/score.sh high high high high high high high high high
bash /workspace/instruments/strategy/score.sh high high high high medium medium medium medium medium
bash /workspace/instruments/strategy/score.sh high low high high high high high high high
```
