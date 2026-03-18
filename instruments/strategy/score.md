# Problem
Score an incoming revenue idea before the agency spends time implementing it.

# Solution
1. Run the scorer with 1-5 ratings for the opportunity:
   - `legality`
   - `consent`
   - `automation_fit`
   - `time_to_cash`
   - `recurring_revenue`
   - `startup_cost`
   - `downside_containment`
   - `data_risk`
   - `reputation_risk`
2. Use this format:

```bash
bash /workspace/instruments/strategy/score.sh \
  legality=5 \
  consent=5 \
  automation_fit=4 \
  time_to_cash=4 \
  recurring_revenue=4 \
  startup_cost=4 \
  downside_containment=5 \
  data_risk=1 \
  reputation_risk=1
```

3. Read the output:
   - `GO` means the idea is eligible to prototype.
   - `HOLD` means controls or clarity are missing.
   - `REJECT` means the idea should be replaced with a compliant alternative.

# Guardrails
- Any idea with weak legality or consent automatically fails.
- High data or reputation risk also forces rejection.
- The tool is for triage, not legal advice.
