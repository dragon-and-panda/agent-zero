# Strategy Scoring Instrument

This instrument scores candidate ventures using a simple PASS or HOLD or REJECT rubric.

## Inputs

Run `score.sh` with six values:

1. legality
2. consent
3. provenance
4. platform_risk
5. durability
6. automation_fit

Accepted values are:

- `low`
- `medium`
- `high`

## Interpretation

- For `legality`, `consent`, and `provenance`, higher is better.
- For `platform_risk`, lower is better.
- For `durability` and `automation_fit`, higher is better.

## Hard gates

- legality `low` => REJECT
- consent `low` => REJECT
- provenance `low` => REJECT
- legality `medium` => HOLD
- consent `medium` => HOLD
- provenance `medium` => HOLD
- platform_risk `high` => HOLD

## Example runs

```bash
./instruments/strategy/score.sh high high high low high high
./instruments/strategy/score.sh medium high high low medium medium
./instruments/strategy/score.sh low high high low high high
```
