# Problem
Build a consent-aware contact dataset from a mailbox export.

# Solution
1. Export your mail as an MBOX file (for example from Google Takeout).
2. Run:
   `bash /a0/instruments/default/email_contact_audit/email_contact_audit.sh <mbox-path> <output-dir> [your_email_1 your_email_2 ...]`
3. Open `<output-dir>/contacts.csv` and `<output-dir>/edges.csv` in Orange for analysis.
4. Before any outreach, manually set `consent_status` per contact and filter out non-opt-in entries.

# Output files
- `contacts.csv`: contact-level counts from From/To/CC/BCC/Reply-To fields.
- `edges.csv`: sender -> recipient frequency graph.
- `summary.json`: run metadata and totals.
