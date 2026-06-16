# Consent Contact Extract Instrument

This instrument filters a CSV down to contacts that are both:

- explicitly consented
- sourced from first-party or client-authorized provenance

It is meant for internal CRM hygiene and client-authorized operations only.

## Not allowed

- preparing lists for resale
- harvesting addresses from mailboxes without authorization
- converting ambiguous inbox data into cold-outreach targets

## Usage

```bash
python3 instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --input contacts.csv \
  --output consent_safe_contacts.csv
```

## Expected columns

Defaults:

- `email`
- `consent`
- `provenance`

You can override the column names with flags.

## Allowed provenance values

- `first_party`
- `client_owned`
- `authorized_export`
- `user_provided`
- `crm`

## Truthy consent values

- `1`
- `true`
- `yes`
- `y`
- `opt_in`
- `consented`

## Output

- a filtered CSV at the requested output path
- a short terminal summary with total, kept, and rejected row counts
