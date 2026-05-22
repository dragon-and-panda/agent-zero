# Strategy Scoring Instrument

Use `score.sh` to screen a revenue lane before activation.

## Hard gates

Every hard gate must be `yes`:

- `legal`
- `consent`
- `provenance`
- `tos`
- `privacy_safe`

If `resale_personal_data=yes`, the lane is automatically rejected.

## Soft factors

Rate each as `low`, `medium`, or `high`:

- `time`
- `margin`
- `repeatability`
- `automation`
- `defensibility`

## Decision rules

- `REJECT`: any hard gate fails or personal-data resale is present
- `PASS`: all hard gates pass, none of the soft factors are `low`, and at least three soft factors are `high`
- `HOLD`: everything else

## Example

```bash
bash instruments/strategy/score.sh \
  --lane "authorized inbox-to-crm" \
  --legal yes \
  --consent yes \
  --provenance yes \
  --tos yes \
  --privacy_safe yes \
  --resale_personal_data no \
  --time medium \
  --margin high \
  --repeatability high \
  --automation high \
  --defensibility medium
```
