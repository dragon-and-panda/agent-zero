# Strategy Scoring Instrument

Use this instrument to score a candidate revenue lane after the compliance pack review.

## Usage

```bash
bash /workspace/instruments/strategy/score.sh \
  <legal> <consent> <provenance> <platform_terms> <delivery> \
  <time_to_cash> <margin> <repeatability> <automation_fit> <defensibility>
```

## Hard Gates

These must be clear or the lane is rejected:

- `legal`: `yes`
- `consent`: `yes`
- `provenance`: one of `first-party`, `client-owned`, `owner-authorized`, `public-business`, `public-nonpersonal`, `synthetic`
- `platform_terms`: `yes`
- `delivery`: `yes`

Any other hard-gate value yields `REJECT`.

## Soft Factors

Use only:

- `high`
- `medium`
- `low`

Soft factors are:

- `time_to_cash`
- `margin`
- `repeatability`
- `automation_fit`
- `defensibility`

## Decision Rule

- `PASS`: every hard gate clears, no soft factor is `low`, and at least three soft factors are `high`
- `HOLD`: hard gates clear, but the lane is not attractive enough yet
- `REJECT`: any hard gate fails
