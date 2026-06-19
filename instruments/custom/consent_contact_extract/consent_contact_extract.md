# Consent Contact Extraction Instrument

This instrument extracts contact emails only from owner-authorized, first-party or licensed data with documented consent.

## Allowed use

- internal CRM cleanup
- opt-in newsletter maintenance
- seller or operator-owned contact exports
- support and account-management workflows

## Disallowed use

- compiling lists for sale
- scraping inboxes without authorization
- exporting contacts from unknown or purchased sources
- preparing unsolicited bulk outreach lists

## Input format

Provide a JSON file containing a list of objects like:

```json
[
  {
    "email": "person@example.com",
    "consent": true,
    "source": "first_party",
    "owner_authorized": true
  }
]
```

## Usage

```bash
python3 instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --input /tmp/contacts.json \
  --output /tmp/consented_contacts.json \
  --owner-authorized \
  --allowed-domains example.com
```

The output contains only accepted contacts plus rejection reasons for skipped records.
