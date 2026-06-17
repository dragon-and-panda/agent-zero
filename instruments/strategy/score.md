# Opportunity Score Instrument

This scoring aid helps autonomous runs decide whether a proposed revenue lane
should be activated, parked, or rejected.

## Inputs

The current shell instrument expects six integer scores from 0 to 10:

- legality
- consent
- repeatability
- time_to_cash
- defensibility
- setup_effort

## Hard Gates

Reject immediately if either of these is true:

- legality < 8
- consent < 8

Examples that should fail the hard gate:

- harvesting personal email addresses without clear permission
- selling contact lists
- spam-style outreach
- reading or processing third-party inboxes without explicit authorization

## Weighted Formula

```text
score = (
  legality*25
  + consent*25
  + repeatability*15
  + time_to_cash*15
  + defensibility*10
  + setup_effort*10
) / 10
```

## Recommendations

- 80 or above: GO
- 65 to 79: HOLD / design more controls
- below 65: REJECT

## Suggested Use

Run this instrument before new automation tracks are promoted into active
execution. Attach the score and rationale to the mission journal.
