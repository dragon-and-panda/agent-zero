# Problem
Prepare a contact export for compliant outreach or CRM hygiene.

# Solution
Use this instrument only on a user-provided CSV that already contains consent and provenance metadata.

Run:
`python /workspace/instruments/custom/consent_contact_extract/consent_contact_extract.py <input_csv> <output_csv>`

# Requirements
- Required columns: `email`, `consent_status`, `provenance`, `allow_marketing`
- Allowed consent values: `opt_in`, `double_opt_in`, `contractual_opt_in`, `customer_opt_in`
- The instrument drops rows that look scraped, bought, or inbox-derived

# Prohibited uses
- Do not point this at Gmail exports, inbox-derived lists, or scraped files.
- Do not use it to prepare a list for resale.
