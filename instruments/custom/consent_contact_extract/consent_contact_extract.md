# Consent Contact Extract

Filter a CSV or JSON contacts file down to records with an email address and documented consent-compatible evidence.

## Purpose

Use this for lawful internal operations such as:

- CRM cleanup
- migration of first-party contact files
- segmentation of opt-in audiences

Do not use it to compile or sell contact lists.

## Accepted inputs

- CSV with header row
- JSON array of objects

## Required evidence

Each returned record must have:

- an email address, and
- either a truthy consent field, or
- a lawful-basis field set to an approved value such as `consent`, `contract`, `customer`, or `vendor`

## Example

```bash
python instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --input work_dir/contacts.csv \
  --email-column email \
  --consent-column consent \
  --lawful-basis-column lawful_basis
```

The script prints JSON with accepted and rejected counts plus the accepted contacts.
