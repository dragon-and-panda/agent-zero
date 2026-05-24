# Strategy Scoring Instrument

Use this instrument to score a monetization lane before operationalizing it.

## Inputs

- legality: yes or no
- consent: yes or no
- provenance: yes or no
- tos: yes or no
- time: high, medium, or low
- margin: high, medium, or low
- repeatability: high, medium, or low
- automation: high, medium, or low
- defensibility: high, medium, or low

## Rules

1. Reject immediately if any hard gate is "no".
2. Pass only if all hard gates are "yes" and no soft factor is "low".
3. Hold if all hard gates are "yes" but one or more soft factors are "low".

## Example

```bash
./instruments/strategy/score.sh \
  legality=yes consent=yes provenance=yes tos=yes \
  time=high margin=medium repeatability=high automation=high defensibility=medium
```
