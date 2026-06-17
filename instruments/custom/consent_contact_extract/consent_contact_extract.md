# Problem
Extract contact rows from a first-party or client-authorized CSV while preserving consent controls.

# Solution
Use this instrument only for first-party CRM hygiene, routing, or suppression management.

Run:

`python3 /workspace/instruments/custom/consent_contact_extract/consent_contact_extract.py <source.csv> <output.csv>`

Requirements:

- input CSV must include `email`, `consent_status`, `source_system`, and `owner_scope`
- only rows with approved consent states are exported
- `owner_scope` must be `first_party` or `client_authorized`
- output is for operational CRM use only, not resale or bulk cold outreach
