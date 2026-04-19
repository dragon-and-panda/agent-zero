## Strategy Opportunity Score

Purpose:
- Score proposed revenue opportunities before execution.
- Reject ideas that depend on privacy abuse, spam, unlawful data brokerage, or platform-rule evasion.
- Create a lightweight PASS / HOLD / REJECT decision that can be used in planning loops.

Inputs:
- `legality`: `low`, `medium`, or `high`
- `consent`: `low`, `medium`, or `high`
- `data_provenance`: `low`, `medium`, or `high`
- `platform_fit`: `low`, `medium`, or `high`
- `automation_leverage`: `low`, `medium`, or `high`
- `time_to_value`: `low`, `medium`, or `high`

Hard gates:
- If legality is `low`, return `REJECT`.
- If consent is `low`, return `REJECT`.
- If data provenance is `low`, return `REJECT`.
- If platform fit is `low`, return `HOLD` unless another hard gate already rejected it.

Scoring:
- Convert `low=1`, `medium=2`, `high=3`.
- Sum all six dimensions.
- `PASS` when score >= 15 and no hard gate triggered.
- `HOLD` when score is between 11 and 14 and no reject gate triggered.
- `REJECT` otherwise.

Output:
- Decision line
- Numeric score
- Concise rationale

Example:
- A consent-based lead magnet plus newsletter sponsorship funnel should typically be PASS.
- A scraped email-list resale idea should be REJECT even if it appears monetizable.
