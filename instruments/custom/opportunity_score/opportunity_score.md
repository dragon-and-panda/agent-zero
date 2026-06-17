# Problem
Score an online venture or monetization idea for compliant autonomous execution.

# Solution
1. Create a JSON file that describes the opportunity, for example:

```json
{
  "name": "AI listing optimization service",
  "customer": "Resellers with poor marketplace conversion rates",
  "offer_type": "service",
  "acquisition_channels": ["seo", "marketplaces", "opt_in_email"],
  "requires_personal_data": false,
  "consent_model": "explicit_opt_in",
  "fulfillment_automation": 0.8,
  "margin_profile": 0.7,
  "time_to_revenue": 0.9,
  "defensibility": 0.5,
  "legal_risk": 0.1,
  "notes": "Start with fixed-price packages and upsell reporting."
}
```

2. Run instrument:

```bash
bash /a0/instruments/custom/opportunity_score/opportunity_score.sh <path-to-json>
```

3. Review the output:
   - weighted score,
   - recommendation (`GO`, `INVESTIGATE`, or `NO_GO`),
   - blockers,
   - reasoning.

4. Reject any idea that depends on list sales, non-consensual personal data use, spam, or platform abuse.
