# Strategy Opportunity Scoring

Use this scorecard before activating a new revenue lane.

## Inputs

Provide six numeric inputs from 0 to 10:

- legality
- consent
- speed_to_cash
- margin
- repeatability
- automation_fit

## Hard Gates

Reject the opportunity immediately if:

- legality < 8
- consent < 8

These two criteria are mandatory because a fast or profitable idea is still unusable if it depends on unlawful or non-consensual behavior.

## Weighted Formula

```text
total =
  legality * 0.25 +
  consent * 0.25 +
  speed_to_cash * 0.15 +
  margin * 0.10 +
  repeatability * 0.15 +
  automation_fit * 0.10
```

## Output Bands

- `GO` if total >= 8.0 and hard gates pass
- `HOLD` if total >= 6.5 and hard gates pass
- `REJECT` otherwise

## Example Reads

- Inbox-to-CRM Hygiene: likely `GO`
- Autonomous Listing Concierge: likely `GO`
- Research Brief Subscription: often `HOLD` until packaging improves
- Personal Email List Brokerage: always `REJECT` because legality and consent fail
