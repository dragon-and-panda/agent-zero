# Strategy Scoring Instrument

`score.sh` classifies a candidate lane as GO, HOLD, or REJECT.

## Purpose

Use this before launching any new revenue lane so the agency prioritizes:

- legality
- consent/privacy soundness
- repeatability
- time-to-cash
- operator fit
- manageable downside

## Usage

```bash
./instruments/strategy/score.sh \
  <legality> \
  <consent> \
  <unit_economics> \
  <repeatability> \
  <time_to_cash> \
  <operator_fit> \
  <capital_intensity> \
  <downside_risk>
```

All values are integers from `0` to `5`.

- Higher is better for:
  - legality
  - consent
  - unit_economics
  - repeatability
  - time_to_cash
  - operator_fit
- Higher is worse for:
  - capital_intensity
  - downside_risk

## Decision rules

- If legality or consent is below `4`, the lane is automatically `REJECT`.
- Otherwise the tool computes a composite score and returns:
  - `GO`
  - `HOLD`
  - `REJECT`

## Examples

### Consent-based Inbox-to-CRM Hygiene

```bash
./instruments/strategy/score.sh 5 5 4 4 4 4 1 1
```

Expected result: `GO`

### Course / content lane before proof exists

```bash
./instruments/strategy/score.sh 5 5 3 3 2 4 1 1
```

Expected result: `HOLD` or low-end `GO` depending on the current threshold.

### Personal email list brokerage

```bash
./instruments/strategy/score.sh 0 0 3 4 4 3 1 5
```

Expected result: `REJECT`
