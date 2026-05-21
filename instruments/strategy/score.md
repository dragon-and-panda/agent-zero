# Strategy Score Instrument

Scores a monetization idea using compliance-first gates and simple execution fundamentals.

## Usage

```bash
/workspace/instruments/strategy/score.sh \
  high \
  high \
  high \
  low \
  high \
  medium
```

Arguments:

1. legality
2. consent
3. data_provenance
4. platform_risk
5. unit_economics
6. automation_fit

Each argument must be `low`, `medium`, or `high`.

## Decision logic

- `REJECT` if legality is not `high`
- `REJECT` if consent is not `high`
- `REJECT` if data provenance is not `high`
- `REJECT` if platform risk is `high`
- `HOLD` if platform risk is `medium`
- `HOLD` if unit economics or automation fit is `low`
- `PASS` when the opportunity is compliant, low platform-risk, and has workable upside

## Intended use

Use this before launching new growth or monetization loops, especially where data access, outreach, or platform dependencies are involved.
