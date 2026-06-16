## Strategy Opportunity Score

Purpose:
- Score proposed revenue opportunities before execution.
- Reject ideas that depend on privacy abuse, spam, unlawful data brokerage, or platform-rule evasion.
- Create a lightweight PASS / HOLD / REJECT decision that can be used in planning loops.

Inputs:
- `legality`: `low`, `medium`, or `high`
- `consent`: `low`, `medium`, or `high`
- `data_provenance`: `low`, `medium`, or `high`
- `platform_risk`: `low`, `medium`, or `high`
- `reversibility`: `low`, `medium`, or `high`

Hard gates:
- If legality is not `high`, return `REJECT`.
- If consent is `low`, return `REJECT`.
- If data provenance is `low`, return `REJECT`.
- If platform risk is `high`, return `HOLD` unless another hard gate already rejected it.

Scoring:
- Convert `low=1`, `medium=2`, `high=3`.
- Sum legality, consent, data provenance, and reversibility.
- `PASS` when score >= 11 and no hard gate triggered.
- `HOLD` otherwise, unless a reject gate triggered.

Output:
- Decision line
- Numeric score when applicable
- Concise rationale tied to the gate or aggregate score

Examples:
- `high high high low high` should typically be `PASS`.
- `high medium high high medium` should typically be `HOLD`.
- `high low high low high` should be `REJECT`.
