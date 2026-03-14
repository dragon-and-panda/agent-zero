# Problem
Extract a deduplicated contact list from authorized Gmail MBOX exports for first-party analysis.

# Solution
1. Ensure you have explicit permission to process the mailbox data.
2. Run:
   - `bash /a0/instruments/default/agentic_financial_system_extract_contacts/agentic_financial_system_extract_contacts.sh --mbox <path_to_mbox> --owner-email <your_email> --output <output_csv_path>`
3. Optional:
   - Pass `--mbox` multiple times for multiple exports.
   - Pass `--owner-email` multiple times if the account has aliases.
4. Import the generated CSV into Orange DataScaping / Orange Data Mining for segmentation and quality checks.

# Output
CSV columns:
- `email`
- `sources` (`received|sent|cc|other`)
- `count_received`
- `count_sent`
- `count_cc`
- `count_other`
- `first_seen`
- `last_seen`
