# Strategy Opportunity Scoring Instrument

This instrument helps Agent Zero evaluate a revenue idea before implementation.

## Purpose

It enforces hard compliance gates first, then scores the remaining business quality signals.

Use it to avoid spending time on opportunities that are illegal, non-consensual, or too dependent on weak data rights.

## Usage

```bash
./instruments/strategy/score.sh \
  "Opportunity name" \
  legality \
  consent \
  data_provenance \
  tos_alignment \
  repeatability \
  monetization_clarity
```

Each rating must be one of:

- `low`
- `medium`
- `high`

## Hard gates

The script immediately blocks opportunities when any of these are weak:

- legality
- consent
- data provenance
- platform terms / TOS alignment

Interpretation:

- `low` on any hard gate -> `REJECT`
- `medium` on any hard gate -> `HOLD`
- all hard gates `high` -> continue to business scoring

## Business scoring

The last two fields describe:

- `repeatability`: can this become a repeatable system rather than one-off hustle work?
- `monetization_clarity`: is the buyer, offer, and revenue mechanism clear?

## Example outcomes

### PASS

```bash
./instruments/strategy/score.sh \
  "CRM cleanup service" \
  high high high high high medium
```

### HOLD

```bash
./instruments/strategy/score.sh \
  "Newsletter sponsorship business" \
  high high high high medium medium
```

### REJECT

```bash
./instruments/strategy/score.sh \
  "Mailbox-derived email list resale" \
  low low low low medium high
```
