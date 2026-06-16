# Strategy Score Instrument

This instrument screens venture candidates with four hard gates and five execution factors.

## Usage

```bash
bash instruments/strategy/score.sh \
  <legality> <consent> <provenance> <platform_risk> \
  <time> <margin> <repeatability> <automation> <defensibility>
```

Each value must be one of:

- `low`
- `medium`
- `high`

## Decision Rules

- `REJECT`: any hard gate is `low`
- `PASS`: all hard gates are at least `medium`, no soft factor is `low`, and at least three soft factors are `high`
- `HOLD`: everything else

Hard gates:

1. legality
2. consent
3. provenance
4. platform_risk

Soft factors:

1. time
2. margin
3. repeatability
4. automation
5. defensibility

## Examples

PASS:

```bash
bash instruments/strategy/score.sh high high high medium medium medium high high high
```

HOLD:

```bash
bash instruments/strategy/score.sh high high high medium low high medium high medium
```

REJECT:

```bash
bash instruments/strategy/score.sh low high high medium high high high high high
```
