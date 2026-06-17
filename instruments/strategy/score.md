# Strategy Scoring Instrument

This instrument provides a simple gate for evaluating candidate revenue lanes before the agent spends time building them.

## Command

```bash
./instruments/strategy/score.sh <legality> <consent> <provenance> <tos> <time> <margin> <repeatability> <automation> <defensibility>
```

Each argument must be one of:

- `low`
- `medium`
- `high`

## Inputs

### Hard Gates

These must all be `high` or the idea is rejected:

1. `legality`
2. `consent`
3. `provenance`
4. `tos`

### Soft Execution Factors

These determine whether a compliant idea is ready now or should be held:

5. `time`
6. `margin`
7. `repeatability`
8. `automation`
9. `defensibility`

## Output States

- `PASS`: Hard gates are clear and every soft factor is strong.
- `HOLD`: Hard gates are clear, but at least one soft factor is not strong enough yet.
- `REJECT`: Any hard gate is not strong.

## Example Runs

```bash
# PASS: compliant and attractive
./instruments/strategy/score.sh high high high high high high high high high

# HOLD: compliant, but weak on automation and repeatability
./instruments/strategy/score.sh high high high high high high medium low medium

# REJECT: unclear consent and provenance
./instruments/strategy/score.sh high medium low high high high high high high
```
