# Problem

Score a proposed revenue lane before building or launching it.

# Solution

1. Describe the lane using the scoring instrument:
   `bash /a0/instruments/strategy/score.sh --lane "<name>" ...`
2. Supply legality, consent, and data provenance honestly. These are hard
   gates, not marketing inputs.
3. Review the output:
   - `PASS` means the lane can move into scoped experimentation.
   - `REJECT` means the lane violates compliance or is too risky to activate.
4. Log the result in:
   - `docs/strategy/incoming.md`
   - `docs/programs/<mission>/journal.md`

# Recommended Inputs

- `--lane`: short lane name
- `--legality`: `strong`, `unclear`, or `weak`
- `--consent`: `explicit`, `owner_only`, `public_business`, `unclear`, or `none`
- `--data`: `first_party`, `client_authorized`, `opt_in`, `public_business`,
  `licensed`, `scraped`, or `unknown`
- `--tos`: `compliant`, `unclear`, or `violating`
- `--automation`: 1-5
- `--time-to-cash`: 1-5
- `--margin`: 1-5
- `--retention`: 1-5
- `--complexity`: 1-5
- `--notes`: free text

# Example

```bash
bash /a0/instruments/strategy/score.sh \
  --lane "Inbox-to-CRM assistant" \
  --legality strong \
  --consent owner_only \
  --data first_party \
  --tos compliant \
  --automation 4 \
  --time-to-cash 4 \
  --margin 4 \
  --retention 3 \
  --complexity 2 \
  --notes "Owner-authorized inbox triage and CRM updates"
```
