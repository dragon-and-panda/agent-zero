# Strategy Opportunity Scoring Instrument

`instruments/strategy/score.sh` scores a revenue opportunity on the factors that matter most for this repository:

- legality and policy fit,
- consent and data safety,
- automation fit,
- speed to cash,
- margin quality,
- repeatability,
- channel redundancy,
- downside protection,
- setup ease.

All inputs use a 0-10 scale where higher is better.

## Usage

```bash
./instruments/strategy/score.sh \
  --name "Listing optimization service" \
  --legality 10 \
  --consent 10 \
  --automation-fit 8 \
  --time-to-cash 8 \
  --margin 7 \
  --repeatability 8 \
  --redundancy 7 \
  --downside-protection 8 \
  --setup-ease 7
```

## Output

The script prints a JSON report with:

- weighted score out of 100,
- qualitative recommendation,
- factor breakdown,
- strongest and weakest factors.

## Interpretation

- `85+`: strong candidate for immediate execution
- `70-84`: viable, but tighten weak points first
- `50-69`: experiment only with guardrails
- `<50`: avoid or redesign

## Suggested initial comparisons

1. Operator-owned listing and resale workflow
2. Productized listing optimization service
3. Tutorial/template/course content lane
4. Authorized inbox-to-CRM cleanup service
5. Any future capital-deployment idea

Use the scores alongside the program charter and compliance pack rather than as a substitute for judgment.
