# Strategy scoring instrument

Purpose:
- score a proposed revenue lane before activation,
- reject workflows with weak legality, weak consent, poor provenance, or high platform risk,
- distinguish strong opportunities from merely acceptable ones.

Inputs:
- legality: low | medium | high
- consent: low | medium | high
- provenance: low | medium | high
- platform_risk: low | medium | high
- time_to_cash: low | medium | high
- margin: low | medium | high
- repeatability: low | medium | high
- automation: low | medium | high
- defensibility: low | medium | high

Hard gates:
- reject if legality is not high
- reject if consent is not high
- reject if provenance is not high
- reject if platform_risk is high

Soft execution factors:
- time_to_cash
- margin
- repeatability
- automation
- defensibility

Decision rules:
- PASS when hard gates clear, no soft factor is low, and at least 3 soft factors are high
- HOLD when hard gates clear but PASS conditions are not met
- REJECT when any hard gate fails

Output:
- one of PASS, HOLD, or REJECT
- plus a short explanation of which gate or factor drove the outcome
