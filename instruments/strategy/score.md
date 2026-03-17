# Opportunity Scoring Instrument

## Purpose

Use this instrument before launching any new revenue offer. It helps the portfolio layer choose opportunities that are fast, lawful, repeatable, and resilient.

## Inputs

Score each dimension from 1 to 5:
- `speed`: time to first dollar
- `margin`: likely contribution margin
- `repeatability`: how easy the offer is to sell repeatedly
- `automation`: how much of delivery can be automated
- `compliance`: legal/privacy/policy safety
- `capital_efficiency`: low up-front cash requirement
- `risk`: delivery, platform, or legal downside
- `complexity`: implementation and ops burden
- `concentration`: dependence on a single platform, supplier, or channel

Interpretation:
- 1 = very weak / very slow / very risky
- 3 = acceptable
- 5 = excellent / very fast / very safe

For penalty dimensions (`risk`, `complexity`, `concentration`), higher scores are worse.

## Usage

```bash
bash /workspace/instruments/strategy/score.sh \
  --name "Listing optimization service" \
  --speed 5 \
  --margin 4 \
  --repeatability 4 \
  --automation 4 \
  --compliance 5 \
  --capital-efficiency 5 \
  --risk 2 \
  --complexity 2 \
  --concentration 3
```

## Output

The instrument prints a JSON summary with:
- normalized benefit score;
- normalized penalty score;
- overall score from 0 to 100;
- recommendation tier;
- gating notes when an opportunity is too risky or non-compliant.

## Decision Heuristic

- `>= 80`: launch candidate
- `65-79`: promising, but improve the weak spots first
- `50-64`: hold for redesign
- `< 50`: reject or park

Any opportunity with low compliance or extreme risk should be rejected even if the numeric score appears attractive.
