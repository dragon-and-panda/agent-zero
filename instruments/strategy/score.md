## Strategy Score Instrument

Purpose:
- evaluate a revenue lane before the agent spends time building it
- reject lanes that fail legality, consent, data provenance, or platform-rules checks
- distinguish between pass, hold, and reject so compliant but weak ideas are not treated as ready

Inputs:
- lane_name: short identifier for the opportunity
- legality: low|medium|high
- consent: low|medium|high
- provenance: low|medium|high
- tos_fit: low|medium|high
- time_to_cash: low|medium|high
- margin: low|medium|high
- repeatability: low|medium|high
- automation: low|medium|high
- defensibility: low|medium|high

Outputs:
- decision: PASS, HOLD, or REJECT
- reason: concise explanation of the gating logic

Rules:
1. Any low value in legality, consent, provenance, or tos_fit produces REJECT.
2. If all hard gates are medium or high but any execution factor is low, produce HOLD.
3. PASS requires every hard gate to be high and every execution factor to be at least medium.
4. High scores across both hard gates and execution factors should receive a PASS with a brief explanation of why the lane is viable.
