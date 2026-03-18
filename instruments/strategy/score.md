# Strategy Scoring Instrument

`score.sh` is a lightweight opportunity triage tool for autonomous revenue programs.

## Purpose
Score a candidate idea before implementation and stop obviously bad ideas early.

## Hard Fail Rules
The script returns `REJECT` immediately when:
- legality is low,
- consent is low,
- or the idea is flagged as privacy-invasive.

## Inputs
Each factor accepts `low`, `medium`, or `high`:
- `--legality`
- `--consent`
- `--margin`
- `--speed`
- `--automation`
- `--defensibility`
- `--redundancy`

Optional:
- `--privacy-invasive yes|no`

## Example
```bash
./instruments/strategy/score.sh \
  --name "Consent inbox CRM cleanup" \
  --legality high \
  --consent high \
  --margin medium \
  --speed medium \
  --automation high \
  --defensibility medium \
  --redundancy high
```

## Interpretation
- `GO`: acceptable for narrow MVP planning
- `HOLD`: improve the design or gather more evidence before launch
- `REJECT`: do not implement
