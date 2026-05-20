## Strategy scoring instrument

Purpose: score a proposed revenue lane before activation.

Hard gates:
- legality: low means reject
- consent: low means reject
- provenance: low means reject
- platform_risk: high means reject

Soft factors:
- time
- margin
- repeatability
- automation
- defensibility

Rules:
- PASS only when all hard gates clear, no soft factor is low, and at least three soft factors are high.
- HOLD when hard gates clear but the opportunity is weak, unclear, or operationally unattractive.
- REJECT when legality, consent, provenance, or platform risk fail.

Usage:
- Run `./instruments/strategy/score.sh legality=high consent=high provenance=high platform_risk=low time=medium margin=high repeatability=high automation=high defensibility=medium`
- Expected outputs: PASS, HOLD, or REJECT
