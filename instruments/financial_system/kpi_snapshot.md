# Problem
Generate a quick KPI summary from JSONL event logs.

# Solution
1. Ensure events are stored as JSON lines (`.jsonl`) with optional keys:
   - `event` (or `type`)
   - `payload.revenue_usd` for revenue aggregation
2. Run:
   `bash /workspace/instruments/financial_system/kpi_snapshot.sh "/path/to/events.jsonl"`
3. Review the summary JSON:
   - `events_total`
   - `parse_errors`
   - `revenue_usd`
   - publication success/failure signals
   - `top_events`
