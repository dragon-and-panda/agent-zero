# Strategy Opportunity Scoring Instrument

Use `score.sh` to score candidate opportunities before implementation.

The instrument is designed for autonomous revenue programs that need hard compliance gates before optimization.

## Inputs

Each factor is scored from `0` to `5`, where higher is better.

- `compliance` - legal and platform safety
- `consent` - strength of consent or relationship basis
- `demand` - evidence that buyers want the offer
- `speed` - how quickly the offer can reach revenue
- `margin` - likely unit economics
- `repeatability` - ease of running the offer more than once
- `automation` - how much of the workflow can be automated safely
- `capital_efficiency` - how little capital the offer needs to start
- `resilience` - ability to survive channel or tool disruption
- `strategic_fit` - alignment with repo capabilities and long-term direction

## Hard gates

The instrument automatically rejects an idea if:

- `compliance < 4`
- or `consent < 4`

This is intentional. Ideas that depend on private-data exploitation or weak consent should be discarded, not tuned.

## Example usage

```bash
bash instruments/strategy/score.sh \
  compliance=5 \
  consent=5 \
  demand=4 \
  speed=4 \
  margin=4 \
  repeatability=4 \
  automation=4 \
  capital_efficiency=5 \
  resilience=4 \
  strategic_fit=5
```

## Interpretation

- `>= 85`: launch candidate
- `>= 70`: incubate and validate
- `>= 55`: research only
- `< 55`: reject or redesign

The output also prints the factor breakdown and whether the idea passed the hard gates.
