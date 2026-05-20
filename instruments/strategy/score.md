# Strategy Score Instrument

This instrument scores a proposed revenue lane after the hard gates are already described.

## Usage

```bash
instruments/strategy/score.sh LEGALITY CONSENT PROVENANCE PLATFORM_RISK TIME MARGIN REPEATABILITY AUTOMATION DEFENSIBILITY
```

All inputs must be `low`, `medium`, or `high`.

## Input meaning

- `LEGALITY`: confidence that the lane is lawful
- `CONSENT`: quality of permission and user authorization
- `PROVENANCE`: quality of the data source
- `PLATFORM_RISK`: risk of breaking platform rules or triggering abuse systems
- `TIME`: expected time to first revenue
- `MARGIN`: expected margin quality
- `REPEATABILITY`: whether the lane can be repeated reliably
- `AUTOMATION`: how well the lane can be automated
- `DEFENSIBILITY`: how durable the lane is against imitation or enforcement

## Decision rules

- `REJECT` if any hard gate is weak:
  - legality is `low`
  - consent is `low`
  - provenance is `low`
  - platform risk is `high`
- `HOLD` if:
  - any hard gate is uncertain (`medium`)
  - any soft factor is `low`
  - fewer than three soft factors are `high`
- `PASS` only if:
  - all hard gates are strong
  - no soft factor is `low`
  - at least three soft factors are `high`

This keeps a real middle state for compliant but unattractive lanes.
