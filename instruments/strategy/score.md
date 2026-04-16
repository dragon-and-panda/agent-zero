# Opportunity Scoring Instrument

This instrument ranks candidate revenue lanes for the agentic financial system.

## Purpose

Use it to compare opportunities with a bias toward:
- legal durability,
- consent and clean data rights,
- speed to revenue,
- strong autonomy fit,
- healthy margins,
- long-term defensibility.

The instrument is intentionally designed to penalize privacy-invasive or non-consensual ideas.

## Input format

Pass a CSV file with the following header:

```csv
name,legality,consent,data_rights,autonomy_fit,time_to_cash,margin,distribution,defensibility,complexity
Inbox-to-CRM Assistant,10,10,10,8,8,7,6,7,4
Autonomous Listing Service,9,9,9,8,6,7,7,6,6
Research Product Studio,9,9,9,7,5,8,5,8,5
```

### Scoring scale
- Use 0 to 10 for every field.
- Higher is better for every field **except** `complexity`.
- `complexity` is treated as a cost and reduces the total score.

## Weights

| Field | Weight |
| --- | ---: |
| legality | 2.0 |
| consent | 2.0 |
| data_rights | 1.5 |
| autonomy_fit | 1.25 |
| time_to_cash | 1.0 |
| margin | 1.0 |
| distribution | 0.75 |
| defensibility | 1.0 |
| complexity | -0.75 |

## Usage

```bash
bash /workspace/instruments/strategy/score.sh /path/to/opportunities.csv
```

The output is a ranked table with:
- weighted score,
- pass/fail gating,
- a recommendation note.

## Automatic rejection rules

The instrument rejects an opportunity if:
- legality < 7,
- consent < 7,
- data_rights < 7.

This is meant to block ideas that might look fast or profitable on paper but create unacceptable compliance risk.
