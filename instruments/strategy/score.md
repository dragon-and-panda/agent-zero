# Strategy Scoring Instrument

Use `score.sh` to quickly classify a monetization lane as `PASS`, `HOLD`, or `REJECT`.

## Hard gates

- legality
- consent
- provenance
- tos

Any hard gate rated low causes `REJECT`.
Any hard gate not rated high causes `HOLD`.

## Soft factors

- time
- margin
- repeatability
- automation
- defensibility

If any soft factor is low, the result is `HOLD`.
If at least three soft factors are high and none are low, the result is `PASS`.
Otherwise the result is `HOLD`.

## Usage

```bash
bash instruments/strategy/score.sh \
  lane="consented inbox-to-crm" \
  legality=high consent=high provenance=high tos=high \
  time=high margin=medium repeatability=high automation=high defensibility=medium
```

## Example outcomes

### PASS

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=high \
  time=high margin=medium repeatability=high automation=high defensibility=medium
```

### HOLD

```bash
bash instruments/strategy/score.sh \
  legality=high consent=high provenance=high tos=high \
  time=low margin=high repeatability=high automation=high defensibility=high
```

### REJECT

```bash
bash instruments/strategy/score.sh \
  legality=low consent=low provenance=low tos=low \
  time=high margin=high repeatability=high automation=high defensibility=high
```
