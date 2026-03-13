# Agentic Financial System — Data & Consent Schema

This schema supports consent enforcement, provenance auditing, outreach controls, and treasury tracking.

## 1) Contacts (canonical)

```sql
CREATE TABLE contacts (
  contact_id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  display_name TEXT,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  source_count INTEGER NOT NULL DEFAULT 0
);
```

## 2) Contact Consent

```sql
CREATE TABLE contact_consent (
  contact_id TEXT NOT NULL,
  contact_status TEXT NOT NULL CHECK (
    contact_status IN ('opt_in', 'transactional_only', 'no_consent', 'do_not_contact')
  ),
  consent_source TEXT,
  consent_captured_at TEXT,
  consent_updated_at TEXT NOT NULL,
  notes TEXT,
  PRIMARY KEY (contact_id),
  FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
);
```

## 3) Provenance (where data came from)

```sql
CREATE TABLE data_provenance (
  provenance_id TEXT PRIMARY KEY,
  contact_id TEXT NOT NULL,
  source_type TEXT NOT NULL, -- gmail_received, gmail_sent, gmail_cc, file_import
  source_ref TEXT NOT NULL,  -- thread/message/file reference
  observed_at TEXT NOT NULL,
  ingestion_run_id TEXT NOT NULL,
  FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
);
```

## 4) Outreach Events

```sql
CREATE TABLE outreach_events (
  event_id TEXT PRIMARY KEY,
  contact_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  event_type TEXT NOT NULL, -- queued, sent, opened, clicked, bounced, unsubscribed
  channel TEXT NOT NULL,    -- email, dm, other
  event_at TEXT NOT NULL,
  compliance_check_passed INTEGER NOT NULL, -- 1 yes, 0 no
  FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
);
```

## 5) Treasury Transactions

```sql
CREATE TABLE treasury_transactions (
  transaction_id TEXT PRIMARY KEY,
  txn_type TEXT NOT NULL, -- revenue, expense, reserve, transfer
  amount_usd REAL NOT NULL,
  occurred_at TEXT NOT NULL,
  source_label TEXT,
  destination_label TEXT,
  reconciliation_ref TEXT,
  tax_reserve_usd REAL NOT NULL DEFAULT 0,
  transfer_confirmation_id TEXT
);
```

## 6) Compliance Queries (examples)

Only opt-in contacts in campaign targeting:

```sql
SELECT c.email
FROM contacts c
JOIN contact_consent cc ON cc.contact_id = c.contact_id
WHERE cc.contact_status = 'opt_in';
```

Find any sent outreach to non-opt-in contacts:

```sql
SELECT oe.event_id, c.email, cc.contact_status, oe.campaign_id, oe.event_at
FROM outreach_events oe
JOIN contacts c ON c.contact_id = oe.contact_id
JOIN contact_consent cc ON cc.contact_id = c.contact_id
WHERE oe.event_type = 'sent'
  AND cc.contact_status != 'opt_in';
```

Monthly transfer reconciliation:

```sql
SELECT substr(occurred_at, 1, 7) AS month, SUM(amount_usd) AS total_transfer
FROM treasury_transactions
WHERE txn_type = 'transfer'
GROUP BY month
ORDER BY month DESC;
```
