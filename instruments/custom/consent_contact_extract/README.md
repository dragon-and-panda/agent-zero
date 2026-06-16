# Consent Contact Extract

This instrument extracts contacts only from structured, authorized files that contain explicit consent signals.

## Allowed use

- client-owned CRM exports
- newsletter subscriber exports with opt-in evidence
- customer or member lists where the user has documented authorization

## Not allowed

- inbox scraping
- contact harvesting from arbitrary files
- building resale lists
- extracting people without explicit permission or a documented business relationship

## Supported inputs

- CSV
- JSON
- JSONL

## Output

Normalized CSV with:

- `email`
- `first_name`
- `last_name`
- `consent_field`
- `consent_value`
- `source_file`

## Usage

```bash
python3 instruments/custom/consent_contact_extract/extract_contacts.py \
  --input contacts.csv \
  --output consented_contacts.csv
```

## Consent detection

The script keeps rows only when it finds an explicit positive value in fields such as:

- `consent`
- `opt_in`
- `email_opt_in`
- `marketing_consent`
- `subscribed`

Rows marked unsubscribed, false, no, or equivalent are excluded.
