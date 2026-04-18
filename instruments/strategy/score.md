# Strategy Opportunity Scoring Instrument

This instrument screens autonomous revenue ideas before the agent invests time or touches external systems.

## Purpose

- Reject illegal, unethical, or non-consensual ideas immediately.
- Preserve a meaningful **HOLD** state for ideas that are compliant but not yet attractive.
- Favor first-party, opt-in, repeatable, and automation-friendly revenue lanes.

## Inputs

Run `score.sh` with the following environment variables:

- `idea` - short lane description
- `legality` - `pass` or `fail`
- `consent` - `pass`, `unknown`, or `fail`
- `provenance` - `pass`, `unknown`, or `fail`
- `tos` - `pass`, `unknown`, or `fail`
- `time` - `high`, `medium`, or `low`
- `margin` - `high`, `medium`, or `low`
- `repeatability` - `high`, `medium`, or `low`
- `automation` - `high`, `medium`, or `low`
- `defensibility` - `high`, `medium`, or `low`

## Output

The script returns one of:

- `PASS` - compliant and operationally attractive
- `HOLD` - compliant but weak on execution or economics
- `REJECT` - blocked by policy or too risky to proceed

## Decision Logic

1. Reject if legality fails.
2. Reject if consent, provenance, or TOS fail.
3. Hold if consent, provenance, or TOS are unknown.
4. Hold if any soft factor is low.
5. Pass only when every hard gate passes and no soft factor is low.
