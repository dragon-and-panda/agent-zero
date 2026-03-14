# Problem
Audit mailbox-derived addresses with a consent-first policy.

# Solution
1. Prepare an `.mbox` mailbox export.
2. (Optional) Prepare a consent file CSV with columns:
   - `email`
   - `consent_status`
3. Run:
   - `bash /a0/instruments/default/consent_contact_audit/consent_contact_audit.sh --mbox /path/to/mailbox.mbox --consent-csv /path/to/consent.csv`
4. Review outputs under `logs/consent_contact_audit`:
   - `discovered_addresses.csv`
   - `eligible_contacts.csv`
   - `blocked_contacts.csv`
   - `summary.json`

## Notes
- Unknown contacts are blocked by default.
- This tool is for compliant segmentation and record-keeping; do not use it for unsolicited outreach or personal-data resale.

