# Agentic Financial System Charter

## Mission

Build a self-sustaining financial system through online ventures that can operate with high autonomy while remaining legal, ethical, auditable, and privacy-safe.

## Non-negotiable constraints

- Follow `docs/policies/compliance_pack.md`.
- Do not rely on selling personal email lists, scraped contacts, or non-consensual data extraction.
- Prefer products, services, workflow automation, research, listings, and opt-in audience assets over data brokerage.
- Treat any inbox, Gmail, or CRM workflow as first-party or client-authorized internal infrastructure, not as a resale asset.

## Operating principles

1. Portfolio over single bet: run multiple compliant lanes with different risk and revenue profiles.
2. Evidence over hype: score each lane before activation and log why it passed, held, or was rejected.
3. Consent first: data provenance and usage rights must be clear before execution.
4. Automation second: automate only after a lane is compliant and commercially plausible.
5. Compounding assets: prefer reusable systems, retained knowledge, and repeatable workflows.

## Initial lane map

| Lane | Description | Revenue model | Status |
| --- | --- | --- | --- |
| Inbox-to-CRM assistant | Use authorized Gmail or mailbox data with RAG to identify warm leads, obligations, and follow-up opportunities for the mailbox owner. | SaaS, setup fees, managed service | Prioritize |
| Autonomous listing service | Turn inputs into marketplace listings and support lifecycle operations. | Service fees, retainers, software | Active hedge |
| Research products | Build reports, watchlists, and market intelligence from public or licensed data. | Subscription, one-off reports, consulting | Active hedge |
| Opt-in audience engine | Create newsletters, lead magnets, and content funnels with explicit consent capture. | Sponsorships, affiliates, paid products | Active hedge |

## Rejected lane

The system must reject any plan centered on compiling or selling email lists, inbox-derived address books, or other personal contact datasets.

## Success metrics

- Number of compliant lanes with PASS status
- Revenue per active lane
- Gross margin and repeatability score
- Automation coverage without compliance regressions
- Audit completeness for data provenance and decisions

## Execution sequence

1. Capture ideas in `docs/strategy/incoming.md`.
2. Screen them with the compliance pack.
3. Score them with `instruments/strategy/score.sh`.
4. Plan approved work with the `revenue_planning` tool.
5. Record decisions, experiments, and outcomes in the program journal.
