# Agentic Financial System — Automation Runbook

Designed for hourly cron triggers (`0 * * * *`) with daily and weekly rollups.

## Hourly Loop

1. **Ingest (5-10 min)**
   - Pull newly available approved email metadata/content.
   - Parse contacts and update consent tags.
   - Append embeddings for fresh context snippets.

2. **Prioritize (5 min)**
   - Score opportunities by fit, urgency, and expected value.
   - Queue only compliant contacts/offers.

3. **Execute (10-20 min)**
   - Run one monetization experiment (outreach batch, offer page test, content CTA).
   - Record campaign IDs and parameters.

4. **Measure (5 min)**
   - Capture outcomes: opens, replies, booked calls, purchases, refunds.
   - Update hourly KPI snapshot.

5. **Journal (2-3 min)**
   - Append one short note to `journal.md`:
     - what changed,
     - what worked/failed,
     - next action.

## Daily Closing Checklist

- Reconcile revenue and expenses.
- Update transfer-ready amount and reserve ratio.
- If transfer criteria pass, prepare transfer instruction to `$Nicsins`.
- Publish short "build in public" summary for content pipeline.

## Weekly Review

- Review top 3 experiments by net profit and repeatability.
- Remove underperforming channels.
- Promote one winning play into a standard operating procedure.
- Update `improvements.md` priorities.

## Core KPIs

- Revenue: gross, net, MRR (if applicable).
- Acquisition: lead-to-reply, reply-to-call, call-to-close.
- Efficiency: CAC, time-to-first-revenue, contribution margin.
- Risk: complaint rate, unsubscribe rate, drawdown (if trading enabled).

## Hard Stops

- Any data-source or consent uncertainty.
- Complaint spike above threshold.
- Trading drawdown breach.
- Missing ledger reconciliation.
