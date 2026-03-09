# Agentic Financial System — Mission Playbook

## 1) Mission Objective
Build a self-sustaining, automated online business system that generates recurring revenue through legal, consent-based operations, then allocates profits into controlled growth strategies.

## 2) Non-Negotiable Guardrails
- Do not collect, store, or sell personal data (including email addresses) without explicit consent and legal basis.
- Do not support spam, unauthorized scraping, phishing, or list-brokering workflows.
- Do not run live high-risk trading before a validated paper-trading phase and risk controls.
- Keep an auditable record of all data sources, consent status, outreach actions, and financial decisions.

## 3) System Architecture (Agentic Framework)

### Core Agents
1. **Orchestrator Agent**
   - Owns goals, schedules, and budget envelopes.
   - Triggers subordinate agents and resolves conflicts.
2. **Toolsmith Agent**
   - Builds and maintains reusable tools/instruments (connectors, ETL, reports).
3. **Data Steward Agent**
   - Enforces consent rules, data minimization, and retention windows.
4. **Monetization Agent**
   - Runs channel experiments and tracks CAC, conversion, and LTV.
5. **Finance/Risk Agent**
   - Handles cashflow reporting, reserve policy, and risk-limited capital allocation.
6. **Content Agent**
   - Produces SOP docs, tutorial modules, and story scripts.

### Shared Components
- **Memory + Knowledge Base:** `memory/` + `knowledge/custom/main/`
- **Program Artifacts:** `docs/programs/financial_system/`
- **Telemetry Logs:** `logs/financial_system/`
- **Compliance Policy Pack:** `docs/policies/financial_data_and_outreach_compliance.md`

## 4) Data Extraction via RAG (Compliant Mode)

### Approved Data Sources
- Gmail data accessible through authorized OAuth scopes.
- Only messages and metadata from accounts with explicit owner permission.
- Optional additional files only when legally owned and consent-cleared.

### Email Intelligence Outputs (Allowed)
- Contact graph and segmentation for first-party relationship management.
- Engagement scoring, topic clustering, and follow-up prioritization.
- Suppression list handling (unsubscribe, no-contact, legal opt-out).

### Disallowed Output
- Any workflow that compiles and sells raw email lists.

## 5) Monetization — Phase 1 (Legal Alternatives)

Replace list-selling with these channels:
1. **Opt-in newsletter sponsorships**
2. **Affiliate partnerships**
3. **Lead-generation with explicit consent capture**
4. **Productized data insights (aggregate, anonymized where required)**
5. **B2B outreach automation to verified business contacts under local law**

### Hourly Execution Loop (Automation-Friendly)
1. Ingest new data and refresh RAG index.
2. Validate compliance state (consent flags, suppression checks).
3. Run one monetization experiment batch.
4. Log KPIs (revenue, conversion, unsubscribes, complaint rate).
5. Append summary to mission diary and update backlog priorities.

## 6) Financial Expansion (Post Phase 1)

### Stage Gate
- Minimum cash reserve target reached.
- 60+ days of stable unit economics.
- No unresolved compliance incidents.

### Trading Rollout (Risk-First)
1. Strategy research and backtest.
2. Paper trading with strict metrics.
3. Small-capital deployment with hard max drawdown and position limits.
4. Weekly risk review; auto-disable on rule violation.

## 7) Financial Management
- Maintain cashflow ledger and payout reconciliation.
- Route distributions only through approved, account-owner-authorized workflows.
- Keep tax documentation and monthly reporting artifacts.

## 8) Content Creation Program

### Required Deliverables
1. **Process Documentation:** SOPs, architecture diagrams, and KPI snapshots.
2. **Course Outline:** Beginner-to-advanced modules for the full system.
3. **YouTube Adaptation Pack:** Script, shot list, hooks, and CTA plan.
4. **Narrative Character Design:** Anthropomorphic narrator persona, visual direction, and story arc.

### Story Premise (Creative Layer)
An anthropomorphic builder chronicles the journey of bootstrapping legal online ventures to fund a mech suit and a synthetic robot body, using transparent metrics and setbacks as narrative beats.

## 9) Success Metrics
- Monthly recurring revenue growth.
- Compliance pass rate (target: 100%).
- List quality and engagement (opt-in growth, low complaint rate).
- Content output cadence (docs + video milestones).
- Capital preservation and risk-adjusted returns.

## 10) Immediate Next Actions
1. Finalize compliance policy pack and consent schema.
2. Build Gmail RAG ingestion pipeline with audit logging.
3. Launch first two monetization experiments (opt-in sponsorship + affiliate).
4. Start weekly tutorial/course production cycle.
5. Track all progress in `journal.md` and `improvements.md`.
