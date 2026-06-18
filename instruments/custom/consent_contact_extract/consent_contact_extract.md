# Consent Contact Extract

Extract contact emails from customer-provided files only when the operator confirms ownership and permission.

## Purpose

This instrument exists for compliant CRM hygiene and segmentation workflows. It is not for scraping mailboxes, harvesting contacts, or creating resale lists.

## Hard limits

- use only on files the customer owns or is authorized to provide
- do not point it at Gmail, mailbox exports, or third-party datasets unless explicit written authorization exists and the use is lawful
- do not use the output for list resale or bulk unsolicited outreach

## Command

```bash
python instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --consent yes \
  --ownership yes \
  --input path/to/export.csv \
  --input path/to/notes.txt
```

## Optional filter

```bash
python instruments/custom/consent_contact_extract/consent_contact_extract.py \
  --consent yes \
  --ownership yes \
  --allow-domain example.com \
  --input path/to/export.csv
```
