# Strategy Scoring Instrument

Use `score.sh` to quickly gate a revenue idea before deeper work.

## Usage

```bash
bash instruments/strategy/score.sh <legality> <consent> <data_provenance> <platform_risk> <repeatability> <margin>
```

Each argument must be `low`, `medium`, or `high`.

## Argument meanings

- `legality`: confidence that the idea is legal in the intended market
- `consent`: quality of user or customer permission for any data or outreach
- `data_provenance`: how trustworthy and first-party the data source is
- `platform_risk`: likelihood of violating platform rules or triggering abuse controls
- `repeatability`: how consistently the offer can be delivered
- `margin`: expected unit economics

For `legality`, `consent`, and `data_provenance`, `high` is best.
For `platform_risk`, `low` is best.

## Decision logic

- `REJECT`: any hard failure on legality, consent, provenance, or platform risk
- `HOLD`: compliance is not clearly bad, but some input needs review or economics are weak
- `PASS`: compliance is strong and the opportunity is economically usable

## Examples

```bash
bash instruments/strategy/score.sh high high high low high high
bash instruments/strategy/score.sh high medium high low medium medium
bash instruments/strategy/score.sh high low high high medium high
```
