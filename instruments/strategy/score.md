# Opportunity Scoring Instrument

Use `score.sh` to classify a revenue lane as PASS, HOLD, or REJECT.

## Hard gates

These must all be clear for a lane to proceed:

- `legality`
- `consent`
- `provenance`
- `tos`

Accepted pass-like values: `pass`, `yes`, `true`, `clear`, `compliant`, `authorized`, `opt-in`, `documented`

Accepted fail-like values: `fail`, `no`, `false`, `unclear`, `unknown`, `scraped`, `unauthorized`, `noncompliant`

Any hard-gate failure returns REJECT.

## Soft factors

These determine whether a compliant lane is attractive enough to activate:

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

Accepted values:

- `high`
- `medium`
- `low`

## Decision rules

- `REJECT`: any hard gate fails or is unclear.
- `HOLD`: hard gates pass, but any soft factor is low or fewer than three soft factors are high.
- `PASS`: all hard gates pass, no soft factor is low, and at least three soft factors are high.

## Example

```bash
bash instruments/strategy/score.sh \
  legality=pass consent=pass provenance=pass tos=pass \
  time=high margin=high repeatability=high automation=medium defensibility=medium
```
