# Problem
Score a revenue opportunity before spending time or budget on it.

# Solution
1. Rate the idea with these inputs:
   - legality confidence: low|medium|high
   - consent quality: low|medium|high
   - data provenance quality: low|medium|high
   - platform risk: low|medium|high
   - unit economics: low|medium|high
2. Run:
   `bash /workspace/instruments/strategy/score.sh <legality> <consent> <provenance> <platform_risk> <unit_economics>`
3. Use the output:
   - PASS means proceed to a small experiment
   - HOLD means fix missing controls first
   - REJECT means do not pursue the idea

# Notes
- Legality and consent must be high for contact-data workflows.
- Platform risk must be low to pass.
- Example rejected idea: selling inbox-derived email lists.
