# Agentic Financial System - Mission Blueprint

This document converts the mission into an executable, autonomous program inside this repository.

## 1) Mission Outcome

Build a self-sustaining online income engine run by agents, then compound capital into disciplined trading and other scalable digital ventures.

## 2) Non-Negotiable Guardrails

The system must remain legal, ethical, and platform-compliant.

- Do not scrape private data without permission.
- Do not harvest or sell personal email lists.
- Do not violate Gmail, Google, or marketplace terms.
- Do not run high-risk live trading before risk controls are validated.
- Keep full audit logs for every automated step.

If a workflow cannot pass these guardrails, the workflow is rejected.

## 3) Operating Model (Agent Responsibilities)

### 3.1 Core Agentic Framework
- **Apex Orchestrator:** Owns priorities, budget, and milestone tracking.
- **Toolsmith Agent:** Builds and maintains instruments and APIs.
- **Data Steward Agent:** Runs ingestion, deduplication, and quality checks.
- **Monetization Agent:** Runs offer creation, funnel tests, and conversion experiments.
- **Treasury Agent:** Handles cashflow, transfer schedules, and reserve policy.
- **Trading Analyst Agent:** Runs strategy research, paper trading, and risk scoring.
- **Media Producer Agent:** Creates documentation, tutorial assets, and video scripts.

### 3.2 Required System Behaviors
- Every decision is tied to a metric.
- Every metric has an owner agent.
- Every sprint ends with a journal entry and backlog refresh.

## 4) Data Extraction and RAG (Compliant Version)

### 4.1 Gmail Data Access
Use OAuth with minimum scopes and explicit account-owner consent. Keep access read-only unless write access is required for a specific approved workflow.

### 4.2 Contact Graph Pipeline
Build a contact graph from:
- Received headers (`From`, `Reply-To`)
- Sent headers (`To`, `Cc`, `Bcc` where available)
- Existing user-owned files and CRM exports

Pipeline steps:
1. Ingest metadata and message snippets needed for business context.
2. Normalize addresses (lowercase, canonical domains).
3. Deduplicate by address and entity.
4. Enrich with relationship tags (client, partner, lead, newsletter subscriber).
5. Store in a CRM-style table with consent status and source.

### 4.3 RAG Usage
- Index only approved content.
- Add policy metadata and retention tags to every chunk.
- Use retrieval for drafting outreach, follow-ups, and support responses.
- Block retrieval of restricted records (missing consent, legal hold, sensitive PII).

### 4.4 Orange DataScaping Role
Use Orange DataScaping for:
- clustering contact segments,
- identifying high-value relationship groups,
- anomaly checks (duplicates, stale entries, missing consent fields).

## 5) Monetization - Phase 1 (Compliant)

Primary objective: generate recurring online revenue from legitimate offers.

Approved channels:
- Productized AI automation services
- Lead qualification and outreach operations for clients (opt-in only)
- Newsletter/media monetization (sponsorships, digital products)
- Templates, playbooks, and premium research packs
- Affiliate programs and partner referrals

Disallowed channel:
- Selling harvested personal email lists.

## 6) Financial Expansion - Post Phase 1

### 6.1 Capital Allocation Sequence
1. Build operating reserve (minimum runway target).
2. Allocate a small experimental sleeve for trading R&D.
3. Scale only after paper-trading and risk thresholds are passed.

### 6.2 Trading Program (Start with Forex Research)
- Phase A: paper trading only
- Phase B: micro-size live tests
- Phase C: scale with strict drawdown and daily loss limits

Minimum controls:
- hard stop-loss rules,
- max portfolio drawdown threshold,
- pre-trade checklist,
- post-trade journaling,
- strategy retirement rules.

## 7) Treasury and Cash Management

- Record all revenue streams and costs in a single ledger.
- Run a scheduled payout process to the designated Cash App account (`$Nicsins`) after reserve and tax allocations.
- Add reconciliation checks so transfer totals match ledger balances.

## 8) Content System

### 8.1 Documentation
- Maintain a living mission diary under `docs/programs/agentic_financial_system/journal.md`.
- Keep a ranked backlog under `docs/programs/agentic_financial_system/improvements.md`.

### 8.2 Course + YouTube Pipeline
1. Capture process recordings and decision logs.
2. Convert logs into lesson modules (foundation, automation, monetization, risk).
3. Generate script + storyboard packs.
4. Publish short and long-form video cuts.

### 8.3 Narrative Character
Create an anthropomorphic narrator persona for a story arc:
- starting constraints,
- milestones of revenue growth,
- setbacks and iteration loops,
- goal of funding a mech suit and robot body.

Use this character consistently across scripts, thumbnails, and recap segments.

## 9) Repo Implementation Plan

### 9.1 Prompt and Agent Layer
- Add persona prompts under `prompts/super-agency/` for the agents listed in Section 3.
- Add guardrail snippets that reject disallowed data monetization requests.

### 9.2 Instruments
- `instruments/finance/ledger_sync.py`
- `instruments/data/contact_graph_builder.py`
- `instruments/monetization/offer_experiment_runner.py`
- `instruments/trading/paper_trade_evaluator.py`
- `instruments/media/script_packager.py`

### 9.3 Extensions
- Budget guard extension for spend limits.
- Compliance extension for consent and data-policy checks.
- Telemetry extension for KPI snapshots per sprint.

## 10) Initial 30/60/90 Plan

### Day 0-30
- Ship consent-aware contact graph MVP.
- Launch first compliant monetization offer.
- Start mission diary and KPI dashboard.

### Day 31-60
- Improve conversion funnel with A/B tests.
- Deploy automated payout/reconciliation flow.
- Begin paper trading with strategy scorecards.

### Day 61-90
- Scale winning offer channels.
- Graduate one strategy from paper to micro-live test.
- Publish first course module and companion YouTube video.

## 11) KPI Set

- Monthly recurring revenue (MRR)
- Gross margin by offer
- Lead-to-client conversion rate
- Contact dataset consent coverage
- Data quality score (duplicates, stale entries, schema completeness)
- Trading paper account expectancy and max drawdown
- Net cash transferred to treasury target (`$Nicsins`)
- Content output cadence (modules/videos per month)

This blueprint is the baseline operating contract for the Agentic Financial System program.
