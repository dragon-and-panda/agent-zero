# Problem
Normalize and deduplicate a contact CSV while keeping only consented records for compliant operations.

# Solution
1. Prepare an input CSV with columns: `email`, `source`, `consent_status`
2. Run:
   `bash /a0/instruments/default/consent_contact_pipeline/consent_contact_pipeline.sh <input.csv> <output.csv>`
3. The script writes:
   - consent-filtered, deduplicated contacts to `<output.csv>`
   - a processing summary to stdout

# Notes
- Allowed output states: `opt_in` and `transactional_only`.
- `unknown` and `do_not_contact` are excluded by design.

