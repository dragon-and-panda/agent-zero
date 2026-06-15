# Problem
Score a venture idea before building it.

# Solution
1. Classify the idea across legality, consent, data provenance, platform risk, automation level, and margin profile.
2. Run:
   `bash /a0/instruments/strategy/score.sh <legal> <consent> <data_provenance> <platform_risk> <automation_level> <margin_profile>`
3. Use one of the supported values:
   - `legal`: `yes` or `no`
   - `consent`: `yes`, `no`, or `unclear`
   - `data_provenance`: `first_party`, `licensed`, `public`, `private`, or `unclear`
   - `platform_risk`: `low`, `medium`, or `high`
   - `automation_level`: `low`, `medium`, or `high`
   - `margin_profile`: `low`, `medium`, or `high`
4. Record the result in `docs/strategy/incoming.md`.

# Example
`bash /a0/instruments/strategy/score.sh yes yes first_party medium high medium`
