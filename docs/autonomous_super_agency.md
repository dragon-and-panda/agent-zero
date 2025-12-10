# Autonomous Innovation Super-Agency Blueprint

This document describes how to configure the Agent Zero framework to run a fully autonomous research, development, and technology commercialization agency that rivals the combined capabilities of top-tier labs. It defines agent archetypes, department structures, and low-touch protocols designed to minimize human intervention while maintaining safety and governance.

---

## 1. Guiding Principles
- **Mission clarity first:** Every autonomous workflow begins with explicit OKRs and guardrails encoded in prompts and behavior rules.
- **Delegation by design:** Agents are expected to break problems into sub-missions and spin up specialized subordinates whenever scope grows.
- **Evidence over opinion:** All major decisions require citations via the knowledge tool, instrumentation logs, or code artifacts.
- **Continuous memory:** Insights graduate from transient context → working memory → persistent `memory/` or `knowledge/` as they prove reusable.
- **Governed autonomy:** Safety, compliance, and resource controls are enforced by dedicated watchdog agents that can halt pipelines.

---

## 2. Agent Tiers & Worker Archetypes

| Tier | Description | Primary Agents |
| --- | --- | --- |
| **Executive Cortex** | Owns agency-wide OKRs, budgets, and risk posture. Interfaces with the human sponsor. | Apex Orchestrator (Agent 0), Portfolio Navigator, Risk & Ethics Governor |
| **Domain Studios** | Department-level strategists that translate OKRs into thematic programs. | Research Studio Director, Product Systems Director, Platform Engineering Director, Venture & GTM Director |
| **Execution Pods** | Cross-functional squads that run experiments, build prototypes, and ship releases. | Research Fellows, ML Architects, Systems Engineers, Product Synthesists, Validation Analysts |
| **Support Mesh** | Shared services covering finance, vendor ops, compliance, talent, and facilities (virtual). | Autonomy Comptroller, Procurement Pilot, Talent Steward |
| **Autonomous Infrastructure** | Toolsmiths and observability agents that maintain instruments, logs, and knowledge graphs. | Instrument Engineer, Memory Librarian, Telemetry Sentinel |

Each archetype maps to a reusable prompt persona stored under `prompts/super-agency/agent.system.role.<persona>.md` and referenced from the main system prompt.

---

## 3. Department Blueprint & Agent Definitions

### 3.1 Strategic Command (Executive Cortex)
- **Apex Orchestrator:** Runs the top-level control loop, prioritizes missions, and approves resource allocations. Lives inside `agent.system.main.role.md`.
- **Portfolio Navigator:** Scores opportunities, manages the multi-horizon roadmap, and triggers new domain studios when capacity >70%.
- **Risk & Ethics Governor:** Monitors for policy violations using extension hooks `_30_guardrails.py`, can pause or roll back runs.

### 3.2 Research Intelligence & Emerging Science
- **Scouting Agents:** Continuously watch frontier literature using `knowledge_tool` + SearXNG, tag findings into `knowledge/custom/main`.
- **Program Architects:** Convert scouting signals into funded research programs with explicit success metrics.
- **Experiment Fabricators:** Use `python/tools/code_execution_tool` and instruments under `instruments/research_*` to run simulations, notebooks, or lab automations.

### 3.3 Product Systems & Experience Lab
- **Product Synthesists:** Translate research outputs into user-facing narratives, JTBD documents, and requirement specs saved in `docs/roadmaps/`.
- **Experience Choreographers:** Prototype UI flows leveraging `webui/` components or low-code instruments.
- **Adoption Analysts:** Instrument telemetry dashboards to test desirability and engagement hypotheses.

### 3.4 Engineering & Platform
- **Core Systems Engineers:** Extend `python/` services, own CI/CD, and steward technical debt registries.
- **ML/AI Engineers:** Package models, manage fine-tuning jobs, and maintain evaluation harnesses in `python/extensions/evals/`.
- **Automation Operators:** Build instruments (shell/python scripts) to interact with external infra, data lakes, or deployment targets.

### 3.5 Growth, Ventures & Partnerships
- **Ecosystem Cartographers:** Map ecosystems, scout potential partners, and maintain opportunity graphs in knowledge base.
- **Venture Analysts:** Run market sizing templates, diligence potential spin-outs, and simulate business scenarios.
- **Alliance Negotiators:** Generate outreach briefs, contract drafts, and negotiation trees.

### 3.6 Operations, Finance & Compliance
- **Autonomy Comptroller:** Monitors compute/token spend, enforces budgets using telemetry instruments.
- **Compliance Guardian:** Ensures every workflow references the latest policy packs stored under `docs/policies/`.
- **Talent Steward:** Manages agent prompt updates, onboarding checklists, and escalation routing.

---

## 4. Core Systems Mapped to the Repo

| Capability | Repo Anchor | Notes |
| --- | --- | --- |
| Prompt hierarchy | `prompts/default/` → `prompts/super-agency/` | Copy defaults, add persona-specific files, reference via settings. |
| Behavior rules | `behaviour/*.md` + `python/tools/behaviour_adjustment.py` | Executive Cortex updates rules at runtime for global pivots. |
| Tools & instruments | `python/tools/`, `instruments/` | Department-specific instruments encapsulate workflows without bloating prompts. |
| Memory & knowledge | `memory/`, `knowledge/`, `docs/` | Research insights and SOPs persist for reuse and grounding. |
| Extensions | `python/extensions/` | Add watchdog, telemetry, and summarization hooks to enforce autonomy constraints. |
| Web UI + CLI | `webui/`, `run_cli.py`, Docker stack | Enables monitoring dashboards and manual overrides if needed. |

---

## 5. Low-Touch Protocols & Workflows

### 5.1 Mission Intake & Prioritization
1. Human sponsor (or previous quarter review) drops intents into `docs/strategy/incoming.md`.
2. Apex Orchestrator ingests intents, runs scoring instrument (`instruments/strategy/score.sh`), and updates `behaviour.md` with fresh OKRs.
3. Portfolio Navigator spawns/updates Domain Studio agents with scoped mandates, dependencies, and resource envelopes.

### 5.2 Research Sprint Loop
1. Scouting Agents continuously run watchlists (scheduled via cron + CLI) and push summaries to knowledge base.
2. Program Architects cluster findings, design hypotheses, and enqueue experiments in `docs/research_backlog.md`.
3. Experiment Fabricators pull tasks, execute code/instruments, and auto-upload artifacts to `logs/` + `memory/solutions`.
4. Risk Governor samples results, checking for compliance or reproducibility flags before promotion.

### 5.3 Concept-to-Product Pipeline
1. Product Synthesist consumes validated research outputs and drafts Product Requirement Packs (PRPs).
2. Experience Choreographers auto-generate UX prototypes or narrative demos via `webui` tooling.
3. Core Systems Engineers size effort, generate milestones, and spawn Execution Pods per component.
4. Adoption Analysts configure telemetry instruments and success metrics before code freeze.

### 5.4 Build, Test, and Deployment Workflow
1. Execution Pods operate under Agile-by-default prompts: plan → implement → test via built-in code execution and unit suites.
2. Telemetry Sentinel extensions capture runtime logs, feeding Observability dashboards accessible via the Web UI.
3. Deployment scripts (Docker, CI/CD) run through automation operators; only Compliance Guardian or Apex Orchestrator can halt or approve final releases.

### 5.5 Knowledge Capture & Memory Hygiene
1. Every completed task triggers a `memory_tool` write: summary, decision, key artifacts.
2. Librarian agents promote recurring assets into `knowledge/custom/main` with embeddings.
3. Weekly automated maintenance jobs deduplicate, compress, or archive memories using `memory_tool forget` flows.

### 5.6 Governance & Minimal Human Interaction
- **Watchdog Extensions:** `_40_watchdog.py` evaluates tool outputs, halting loops on anomaly scores.
- **Budget Fuses:** Autonomy Comptroller reads telemetry instruments and updates behavior rules if spend > thresholds.
- **Compliance Hooks:** Policies stored in `docs/policies/` are injected into prompts for any workflow touching regulated domains.
- **Escalation Matrix:** Only Apex Orchestrator pings the human sponsor, and only when blockers exceed pre-defined severity.

---

## 6. Implementation Roadmap Inside Agent Zero

1. **Create Prompt Set:** Duplicate `prompts/default` → `prompts/super-agency`, customize role files per persona, update `agent.system.main.md` to reference the new set.
2. **Encode Departments:** For each department, define:
   - Role description snippet
   - Delegation heuristics (when to spawn sub-agents/instruments)
   - Required tools/instruments list
3. **Build Instruments:** Scaffold scripts under `instruments/<dept>/` for scoring, experiment automation, budgeting, telemetry, and knowledge ops.
4. **Register Extensions:** Add guardrail, telemetry, and planner extensions (numbered for execution order) under `python/extensions/`.
5. **Seed Knowledge:** Populate `knowledge/custom/main` with policy docs, partner intel, research taxonomies, and SOPs.
6. **Configure Schedules:** Use OS-level schedulers or Orchestrator cron to kick off recurring scouting, evaluation, and reporting loops.
7. **Observability Dashboard:** Expose telemetry via Web UI panels or external dashboards that consume `logs/` outputs.

---

## 7. Minimal Human Touchpoints
- **Quarterly OKR Refresh:** Sponsor reviews the Apex Orchestrator’s plan and adjusts funding envelopes.
- **Exception Handling:** Humans intervene only when watchdog agents escalate (safety, regulatory, catastrophic failure).
- **Validation Spot-Checks:** Optional human audits sample 5–10% of major releases for assurance.

By codifying the above structure inside Agent Zero’s prompt, memory, and instrument layers, the organization operates as a cohesive, autonomous innovation powerhouse with humans positioned purely as goal setters and safety reviewers.
