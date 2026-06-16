# Consent Contact Extract Instrument

This instrument converts first-party contact records into a CRM-ready CSV while enforcing a simple rule:

Only rows with explicit consent signals are allowed through.

## Intended use

- customer-owned contact exports
- consented CRM data cleanup
- subscriber list normalization

## Forbidden use

- scraping inboxes or websites for email addresses
- extracting contacts for resale
- creating unsolicited outreach lists

## Input formats

- CSV with headers
- JSON array of objects

## Output

- CSV containing unique, consented contacts
- JSON summary with counts

## Example

```bash
python3 instruments/custom/consent_contact_extract/extract_contacts.py \
  --input contacts.csv \
  --output consented_contacts.csv \
  --report report.json
```
