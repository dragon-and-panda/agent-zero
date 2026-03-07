# Ethical Agentic Financial System Playbook

This playbook translates the mission into a lawful, durable operating model.

## 1) Non-negotiable constraints

- Process only data you own or have explicit permission to use.
- Do not buy, scrape, or sell personal email lists without consent.
- Follow CAN-SPAM, GDPR, CCPA, and local privacy/marketing laws.
- Keep auditable records for consent, suppression, and data retention.

## 2) Agentic framework architecture

### Core loop

1. **Acquire**: ingest approved data sources (mailbox exports, CRM, web analytics).
2. **Structure**: normalize entities (contacts, companies, interactions).
3. **Score**: rank opportunities (engagement, intent, fit).
4. **Act**: run approved actions (content publishing, outreach to opted-in audiences, product updates).
5. **Measure**: track conversion, CAC, LTV, and net cash flow.
6. **Refine**: retrain prompts/heuristics based on outcomes.

### Required components

- Runtime orchestration: this repository's multi-agent stack.
- Knowledge + RAG: curated docs in `knowledge/custom/`.
- Reusable instruments: scripts in `instruments/default/` or `instruments/custom/`.
- Logging + memory: keep weekly reviews and postmortems in `memory/`.

## 3) Email data extraction (compliant implementation)

Use `python/helpers/email_contact_extractor.py` to convert authorized mailbox exports into Orange-friendly CSV.

Example:

```bash
python -m python.helpers.email_contact_extractor \
  --input "/path/to/google-takeout-mail" \
  --out-csv "/tmp/contacts_for_orange.csv" \
  --out-json "/tmp/contacts_summary.json" \
  --owner-email "you@example.com" \
  --min-mentions 2
```

### Supported data sources

- `.mbox` mailbox export files
- `.eml` raw emails
- `.txt`, `.csv`, `.json`, `.md`, `.log` text files

### Orange workflow

1. Import `contacts_for_orange.csv`.
2. Filter low-quality rows (`total_mentions < threshold`).
3. Create segments (customers, partners, vendors, media, unknown).
4. Build outreach/sales experiments only for opted-in segments.

## 4) Monetization Phase 1 (replace list-selling)

Instead of selling raw contact data, monetize through:

- Productized services (research, automation setup, content pipelines)
- Affiliate content + SEO pages
- Newsletter sponsorships for opted-in audiences
- Digital products (templates, playbooks, automation kits)
- B2B lead research from public/professional datasets with clear compliance

Success metrics:

- Weekly qualified opportunities generated
- Revenue per channel
- Gross margin and payback period

## 5) Financial expansion (post Phase 1)

Before trading:

- Build emergency reserve and tax reserve.
- Use paper trading and backtests first.
- Set max drawdown, position sizing, and hard stop-loss rules.
- Track expectancy and risk-adjusted return before scaling.

If moving into forex, enforce strict risk policy:

- Risk per trade <= 0.5% to 1.0% of account
- Daily max loss cap
- No strategy changes mid-session without review

## 6) Cash management operations

- Maintain a simple ledger: revenue, expenses, taxes, reserves, owner distributions.
- Schedule transfer cadence and reconciliation checklist.
- If using a cash app handle, keep transfer records and settlement proofs.

## 7) Documentation and content system

Create one artifact per week:

- **Ops log**: what was tried, what worked, what failed.
- **Tutorial module**: one repeatable workflow with screenshots.
- **Video script**: convert module into short-form and long-form scripts.

### Story framework (anthropomorphic narrator)

- Character: a builder-pilot funding a mech/robot project.
- Arc: chaos -> systems -> first cashflow -> compounding engine.
- Rule: every chapter includes one real metric and one practical lesson.

## 8) 30-day execution cadence

- **Week 1**: set constraints, ingest data, build first scoring model.
- **Week 2**: launch two compliant offers and one content funnel.
- **Week 3**: optimize conversion and automate repetitive tasks.
- **Week 4**: publish monthly review, update risk limits, plan next sprint.
