# Strategy Scoring Instrument

`score.sh` gives a quick PASS, HOLD, or REJECT verdict for a venture idea.

## Inputs

Run:

```bash
./instruments/strategy/score.sh legality consent provenance platform_risk margin speed defensibility
```

Each input must be `low`, `medium`, or `high`.

### Meaning

- `legality`: confidence that the plan is lawful
- `consent`: confidence that required permission exists for personal-data use
- `provenance`: confidence that data sources are documented and clean
- `platform_risk`: risk of violating marketplace, API, or channel rules
- `margin`: likely gross margin
- `speed`: how quickly the idea can be tested
- `defensibility`: how hard it is to copy

For the first three fields, `high` is best.
For `platform_risk`, `low` is best.

## Hard gates

- `legality != high` -> reject
- `consent == low` -> reject
- `provenance == low` -> reject
- `platform_risk == high` -> reject
- `consent == medium` or `provenance == medium` -> hold until clarified

## Example

```bash
./instruments/strategy/score.sh high high high low medium high medium
```
