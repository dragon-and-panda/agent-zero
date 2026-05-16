# Strategy Opportunity Scoring Instrument

This instrument scores candidate revenue lanes for the Agentic Financial System.

## Purpose

Reject ideas that are risky, non-consensual, or likely to violate platform terms before any implementation work begins.

## Usage

```bash
./instruments/strategy/score.sh \
  "Inbox-to-CRM" \
  legality=high \
  consent=high \
  provenance=high \
  tos=high \
  automation=high \
  time_to_cash=medium \
  differentiation=medium \
  ops_burden=medium
```

## Required Fields

- `legality`
- `consent`
- `provenance`
- `tos`
- `automation`
- `time_to_cash`
- `differentiation`
- `ops_burden`

Accepted values: `low`, `medium`, `high`

## Decision Rules

- **REJECT** if any of `legality`, `consent`, `provenance`, or `tos` is `low`
- **HOLD** if no hard reject applies but total score is weak or one of the core risk factors is only `medium`
- **PASS** when the core risk factors are strong and the weighted score is high enough

## Interpretation

This tool is intentionally conservative. It should block questionable growth ideas early and push the program toward durable, compliant monetization paths.
