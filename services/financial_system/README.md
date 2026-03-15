# Financial System Tools (Compliant Data Intelligence)

This folder contains runnable tooling for the financial-system program defined in `docs/autonomous_financial_system.md`.

## Tool: Contact Intelligence Extractor

`tools/extract_contact_intelligence.py` scans authorized mailbox exports and related files, then builds:

- `contacts.csv`: canonical contact table with counts by channel (`from`, `to`, `cc`, `bcc`, `reply_to`, `other`),
- `domains.csv`: domain-level aggregates,
- `summary.json`: run metadata and quality signals.

### Supported Inputs

- `.mbox`
- `.eml`
- `.csv`, `.tsv`
- `.json`
- `.txt`, `.md`, `.log`

### Quick Start

```bash
cd services/financial_system
python tools/extract_contact_intelligence.py \
  --input /path/to/mail_exports \
  --input /path/to/other_files \
  --output-dir /tmp/contact_intel
```

Optional consent mapping:

```bash
python tools/extract_contact_intelligence.py \
  --input /path/to/mail_exports \
  --output-dir /tmp/contact_intel \
  --consent-file /path/to/consent_status.csv
```

`consent_status.csv` should contain at least:

```text
email,status
alice@example.com,opt_in
bob@example.com,opt_out
```

Accepted status values: `opt_in`, `opt_out`, `suppressed`, `unknown`.

## Orange DataScaping Usage

1. Open Orange.
2. Load `contacts.csv` with a File widget.
3. Add Select Columns, Data Table, and Rank/Cluster widgets.
4. Use `total_mentions`, channel counts, and consent status for segmentation and QA.
5. Join with `domains.csv` for domain-level quality and concentration analysis.

## Compliance Note

This tool is for first-party analytics on authorized data. Do not use outputs for spam, unauthorized outreach, or personal-data resale.
