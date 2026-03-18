# Strategy Scoring Instrument

`instruments/strategy/score.sh` scores candidate ventures so the agent can prioritize revenue ideas consistently.

## Factors

Each factor is scored from 1 to 5:

- **acquisition** - How reliably customers can be found.
- **delivery** - How easily the offer can be fulfilled with current repo assets and automation.
- **compliance** - How clean the legal / privacy / platform posture is.
- **speed** - How quickly the first paid delivery could happen.
- **margin** - Expected contribution margin after direct costs.
- **durability** - Chance the offer can compound into a repeatable business.
- **capital** - Low capital requirement gets a higher score.

## Decision thresholds

The script reports both raw and weighted totals, but makes decisions using the weighted score so compliance has extra influence.

- **GO**: weighted score >= 29 and compliance >= 4
- **HOLD**: weighted score >= 23 and compliance >= 3
- **REJECT**: anything below HOLD, any explicit violation flag, or any forbidden pattern

## Forbidden patterns

The script auto-rejects ideas if the name or notes suggest:

- selling email lists,
- inbox scraping for resale,
- spam-first models,
- credential abuse,
- pump-and-dump style schemes,
- leverage-first Forex strategies.

## Example

```bash
./instruments/strategy/score.sh \
  --name "Inbox-to-CRM Hygiene Service" \
  --acquisition 4 \
  --delivery 4 \
  --compliance 5 \
  --speed 4 \
  --margin 3 \
  --durability 4 \
  --capital 5
```

## Output

The script prints:

- weighted total,
- raw score,
- decision,
- notes about any policy flags.
