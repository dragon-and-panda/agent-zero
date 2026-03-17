# Problem

Rank candidate revenue opportunities before launching them.

# Solution

Use the strategy scoring instrument to compare opportunities on compliance, time-to-cash, automation leverage, margin, repeatability, resilience, strategic fit, and capital efficiency.

## Guardrails

- Do not score opportunities that depend on selling personal email lists, scraped contact data, unsolicited bulk outreach, or deceptive acquisition.
- If compliance is below the threshold, the instrument will reject the opportunity.

## Run

```bash
bash /workspace/instruments/strategy/score.sh \
  "Managed listing concierge" \
  10 8 7 8 7 8 9 8
```

Arguments after the opportunity name must be integers from 0 to 10 in this order:

1. compliance
2. time_to_cash
3. automation_leverage
4. margin
5. repeatability
6. resilience
7. strategic_fit
8. capital_efficiency

## Interpretation

- A higher overall score means the opportunity fits the program better.
- Compliance below `8` is an automatic rejection.
- Use the output to compare a primary offer and at least one fallback offer so the revenue plan has redundancy.
