# Consent Contact Extract Instrument

This instrument extracts email addresses only from owner-authorized files for first-party or client-authorized workflows.

## Allowed uses

- CRM cleanup
- deduplication of opted-in customer contacts
- support mailbox cleanup for the data owner
- migration of lawful first-party contact records

## Disallowed uses

- building lists for resale
- harvesting inbox contacts for third-party outreach
- extracting contacts from private data without documented authorization

## Usage

```bash
python3 instruments/custom/consent_contact_extract/extract.py \
  --owner-authorized yes \
  --consent-basis opted_in \
  --output /tmp/contacts.csv \
  --input /path/to/export1.txt \
  --input /path/to/export2.csv
```

Optional:

- `--domain-allowlist example.com` to keep only approved domains

## Output columns

- `email`
- `source_file`
- `consent_basis`

The output is intended for first-party hygiene workflows, not resale or cold outreach.
