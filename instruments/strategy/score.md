# Strategy Opportunity Score

This instrument scores a proposed revenue opportunity before time or money is committed.

It is designed to favor lawful, consent-based, high-margin, repeatable bets and to penalize ideas that are overly dependent on a single platform, high capital outlay, or elevated regulatory exposure.

## Inputs

Rate each input from 1 to 5:

- `legal` - how clearly lawful and policy-compliant the opportunity is
- `consent` - how strong the permission and data-rights posture is
- `automation` - how much of the workflow can be systematized
- `margin` - likely unit economics
- `time_to_cash` - speed to first revenue
- `repeatability` - ability to deliver or sell more than once
- `resilience` - ability to survive channel/platform disruption
- `platform_dependency` - reliance on a single marketplace or platform
- `capital_intensity` - up-front cash required
- `regulatory_exposure` - compliance complexity or downside risk

## Usage

```bash
./instruments/strategy/score.sh \
  --name "AI Workflow Audit" \
  --legal 5 \
  --consent 5 \
  --automation 4 \
  --margin 4 \
  --time-to-cash 4 \
  --repeatability 4 \
  --resilience 4 \
  --platform-dependency 2 \
  --capital-intensity 1 \
  --regulatory-exposure 1
```

## Output

The script prints:

- the weighted score,
- a decision band,
- a short interpretation,
- the highest-risk inputs to improve before launch.

## Suggested Decision Bands

- `80+` - strong candidate, proceed with launch planning
- `65-79` - good candidate, add guardrails or de-risk weak inputs
- `50-64` - sandbox only, not ready for primary focus
- `<50` - reject or redesign

## Operating Rule

If `legal` or `consent` is below `4`, the opportunity should not be promoted into active execution even if the total score is high.
