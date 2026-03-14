# Email Contact Extractor Instrument

This instrument builds a deduplicated contact table from exported email data.

## Purpose

Use it to organize your own inbox/sent archives for CRM, relationship mapping, and opt-in outreach planning.

> [!IMPORTANT]
> Do not use extracted contacts for spam, unauthorized data sales, or any activity that violates privacy laws or platform terms.

## Supported inputs

- `.mbox` exports (for example, Google Takeout Mail exports)
- `.eml` files
- `.txt` files (regex scan fallback)

## What it extracts

- `From`, `To`, `Cc`, `Reply-To`, `Sender`, and `Resent-*` addresses
- Optional `Bcc` extraction (when present in exported source)
- First and last seen timestamps (when message `Date` header is available)
- Source headers used for each contact

## Usage

From repo root:

```bash
python instruments/custom/email_contact_extractor/extract_contacts.py "/path/to/mail_export" --output-csv "/path/to/contacts.csv"
```

Exclude internal or personal domains:

```bash
python instruments/custom/email_contact_extractor/extract_contacts.py "/path/to/mail_export" \
  --exclude-domain yourcompany.com \
  --exclude-domain gmail.com \
  --output-csv "/path/to/contacts_external.csv"
```

Include BCC headers (if your export contains them):

```bash
python instruments/custom/email_contact_extractor/extract_contacts.py "/path/to/mail_export" --include-bcc
```

## Orange DataScaping / Orange Data Mining workflow

1. Generate `contacts.csv` with this instrument.
2. Open Orange and load the CSV with **File** widget.
3. Use **Data Table**, **Select Rows**, **Distributions**, and **Scatter Plot** to segment contacts by:
   - domain
   - interaction frequency (`message_count`)
   - recency (`last_seen`)
4. Build permission-aware cohorts (for example: existing customers, inbound leads, collaborators) before any outreach.

## Output schema (`contacts.csv`)

- `email`
- `name`
- `message_count`
- `first_seen` (ISO-8601, UTC when available)
- `last_seen` (ISO-8601, UTC when available)
- `sources` (semicolon-separated header list)
