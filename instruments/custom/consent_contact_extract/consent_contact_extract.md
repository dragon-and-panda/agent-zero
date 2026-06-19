# Consent-Only Contact Extraction

Use this instrument only for owner-authorized, first-party contact datasets where consent and provenance have been documented.

## What it does

- reads a JSON list of contact records
- validates email format
- filters contacts to allowed domains
- requires owner authorization at the dataset level or per record
- rejects scraped, purchased, brokered, leaked, or inbox-derived contact records

## Input requirements

The input file must contain a JSON array of objects. Each object may include:

- `email`
- `owner_authorized`
- `consent`
- `provenance`
- `notes`

## Usage

```bash
python3 instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --input contacts.json \
  --allowed-domains example.com,customer.org \
  --owner-authorized
```

## Decision logic

A record is accepted only if:

- the email is valid
- the domain is in `--allowed-domains`
- the dataset is owner-authorized or the record has `owner_authorized=true`
- the record has `consent=true`
- the provenance is first-party and not scraped, purchased, brokered, leaked, or inbox-derived
