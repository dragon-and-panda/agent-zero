# Problem
Extract and organize contact emails from authorized communication exports.

# Solution
1. Export your own mailbox data (for example via Google Takeout `.mbox` files).
2. Run:
   - `bash /a0/instruments/default/email_contact_intel/email_contact_intel.sh --mbox /path/to/mailbox.mbox --owner you@example.com`
3. Optional:
   - Add more mailboxes with another `--mbox ...`
   - Scan extra files with `--file /path/to/notes.txt`
   - Keep only frequent contacts with `--min-count 2`
4. Outputs are written to `output/email_contact_intel/` by default:
   - `contacts.csv`
   - `contacts.json`
   - `summary.json`

# Notes
- This tool is for data you own or are authorized to process.
- Use output for compliant, permission-based workflows only.
