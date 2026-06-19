# Strategy Scoring Instrument

This instrument scores a monetization idea across four risk gates:

- legality risk
- consent risk
- provenance risk
- platform risk

## Usage

```bash
./instruments/strategy/score.sh <legality> <consent> <provenance> <platform>
```

Each argument must be one of:

- `low`
- `medium`
- `high`

## Decision Rules

- `REJECT` if legality or consent risk is `high`
- `HOLD` if provenance or platform risk is `high`
- `HOLD` if any factor is `medium`
- `PASS` only when all four factors are `low`

## Example

```bash
./instruments/strategy/score.sh high high high high
./instruments/strategy/score.sh low medium low low
./instruments/strategy/score.sh low low low low
```
