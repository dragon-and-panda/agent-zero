# Problem
Build a deduplicated contact ledger from first-party mailbox data.

# Solution
1. Prepare consented mailbox inputs (`.mbox` or `.eml`) and optional consent CSV.
2. Run:
   - `bash /a0/instruments/default/email_contact_extractor/email_contact_extractor.sh --input <mailbox_or_dir> --output-csv <output.csv>`
3. Review outputs:
   - contacts CSV (deduplicated addresses with source roles)
   - summary JSON (`<output.csv>.summary.json`)

# Notes
- For compliance, only use data you are authorized to process.
- Do not use this workflow for unsolicited outreach or list resale.
- Optional consent CSV headers: `email,consent_status,suppressed`
