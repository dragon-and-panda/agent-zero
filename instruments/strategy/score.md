## strategy scoring instrument

Purpose:
- score a proposed revenue lane before activation
- reject lanes that depend on privacy abuse, non-consensual outreach, personal-data resale, deception, or terms-of-service evasion
- allow compliant lanes to pass only when they also show real execution quality

Hard gates:
- legality: PASS or FAIL
- consent: PASS or FAIL
- provenance: PASS or FAIL
- platform_terms: PASS or FAIL

If any hard gate fails, overall result is REJECT.

Soft factors:
- time_to_cash: low, medium, high
- margin: low, medium, high
- repeatability: low, medium, high
- automation_fit: low, medium, high
- defensibility: low, medium, high

Decision policy:
- PASS when every hard gate passes, no soft factor is low, and at least three soft factors are high
- HOLD when every hard gate passes but the soft factors do not yet justify activation
- REJECT when any hard gate fails

Examples:
- opt-in inbox triage service for founder-owned Gmail -> likely HOLD or PASS depending on economics
- selling scraped email lists -> REJECT
- consent-based local business listing optimization service -> PASS candidate
