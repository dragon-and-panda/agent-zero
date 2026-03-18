# Problem
Score new revenue ideas before launching them.

# Solution
1. Run the instrument with named flags:
   `bash /a0/instruments/strategy/score.sh --idea "Inbox-to-CRM Hygiene Service" --legality 5 --automation 4 --time-to-cash 4 --repeatability 5 --capital-efficiency 5 --redundancy 4 --execution-risk 2 --consent yes --third-party-data no --regulated no`
2. Review the decision:
   - `GO` means the idea can move into packaging and proof-building.
   - `HOLD` means the idea needs more controls or validation.
   - `REJECT` means it conflicts with the compliance rules or scores too poorly.
3. Record the result in `docs/strategy/incoming.md`.

# Notes
- `consent=no` or `third-party-data=yes` automatically triggers `REJECT`.
- Use a 0 to 5 scale for all numeric inputs.
- Lower `execution-risk` is better.
