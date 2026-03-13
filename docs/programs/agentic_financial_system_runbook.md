# Agentic Financial System — Operations Runbook

This runbook translates the blueprint into recurring operating procedures.

## 1) Daily Loop

1. Ingest new authorized sources (Gmail metadata, approved files).
2. Normalize and deduplicate contact records.
3. Run consent audit before any outreach activity.
4. Execute active monetization workflows.
5. Record treasury inflows/outflows and reconciliation status.
6. Capture daily summary in mission diary.

## 2) Weekly Loop

1. Review KPI snapshot (revenue, consent safety, outreach quality, ops throughput).
2. Process suppression/deletion queue.
3. Review improvement backlog priorities.
4. Update content plan and publish one educational artifact.
5. Evaluate paper-trading metrics (if applicable).

## 3) Pre-Outreach Checklist

- Contact dataset has required fields.
- `contact_status` values are valid.
- Campaign target set contains only `opt_in`.
- Suppression list applied and verified.
- Audit output archived with timestamp.

If any check fails, outreach is blocked.

## 4) Treasury Transfer Checklist (Cash App: `$Nicsins`)

- Reconcile source revenue entries.
- Confirm reserve and tax allocation.
- Execute transfer and capture confirmation ID.
- Log transaction in treasury table/ledger.
- Attach evidence in weekly review notes.

## 5) Instrument Commands

Consent audit:

```bash
bash /workspace/instruments/financial_system/consent_audit.sh "/path/to/contacts.csv" outreach
```

KPI snapshot from JSONL events:

```bash
bash /workspace/instruments/financial_system/kpi_snapshot.sh "/path/to/events.jsonl"
```

## 6) Escalation

Escalate immediately if:
- non-opt-in outreach is detected,
- restricted data appears in unauthorized export targets,
- treasury mismatches are unresolved within one cycle.

On escalation:
1. Pause automations touching impacted scope.
2. Preserve logs and affected artifacts.
3. Open remediation items in improvement backlog.
