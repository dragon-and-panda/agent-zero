# Strategy Scoring Instrument

This instrument gives each candidate revenue idea a simple governance verdict:

- PASS: acceptable to explore now
- HOLD: missing clarity or controls
- REJECT: incompatible with policy

## Inputs

Run the script with four values:

```bash
./instruments/strategy/score.sh <legality> <consent> <data_provenance> <platform_risk>
```

Allowed values:

- `low`
- `medium`
- `high`

Interpretation:

- `legality`: confidence the activity is lawful
- `consent`: quality of the permission basis for any personal data use
- `data_provenance`: confidence the data source is authorized, public, licensed, or first-party
- `platform_risk`: risk of violating marketplace, API, or anti-abuse rules

## Decision Rules

- reject if legality is low
- reject if consent is low
- reject if data provenance is low
- reject if platform risk is high
- hold if any remaining value is medium
- pass only when legality, consent, and data provenance are high and platform risk is low

## Examples

```bash
./instruments/strategy/score.sh high high high low
./instruments/strategy/score.sh high medium high low
./instruments/strategy/score.sh high low high low
```
