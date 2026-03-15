# Problem
Extract a clean list of consented email contacts from CSV exports.

# Solution
1. Prepare a CSV with at least:
   - an email column (default: `email`)
   - a consent column (default: `consent_status`)
2. Run:
   `bash /a0/instruments/custom/consent_contact_extract/consent_contact_extract.sh <input_csv> <output_dir>`
3. Review outputs in `<output_dir>`:
   - `consented_emails.txt` (deduped)
   - `domain_counts.csv`
   - `invalid_rows.csv`

# Notes
- This instrument is for first-party or authorized data only.
- It does not fetch mailbox data and does not support scraping or list brokering.
