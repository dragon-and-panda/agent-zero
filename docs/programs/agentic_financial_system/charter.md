# Agentic Financial System Charter

## Mission

Build a self-sustaining, ethically operated financial system using Agent Zero
to research, launch, and improve online revenue ventures with minimal human
supervision.

## Non-Negotiable Constraints

All work in this program must comply with
`docs/policies/compliance_pack.md`.

The following are explicitly out of scope:

- harvesting email addresses from Gmail or files for resale,
- selling personal contact databases,
- automating spam or deceptive outreach,
- monetization models that rely on unclear data provenance.

## Safe Interpretation of the Current Mission

The original mission direction included monetization ideas involving compiled
email lists. That lane is rejected. The compliant replacement is:

1. Use email/RAG only for owner-authorized operational workflows.
2. Build products and services that monetize automation, not private contact
   extraction.
3. Prioritize first-party or clearly licensed data and explicit customer value.

## Phase 1 Revenue Lanes

### Lane A: Inbox-to-CRM Operations Assistant

Use owner-authorized or client-authorized inbox data to:

- classify inbound messages,
- extract leads that already contacted the business,
- summarize intent,
- create CRM records,
- draft compliant follow-ups for review or approved automation.

**Monetization model:** subscription service, setup fee, or managed operations
retainer.

### Lane B: Autonomous Listing Service

Extend the blueprint in `docs/autonomous_listing_service.md` and the scaffold in
`services/autonomous_listing/` into a sellable listing concierge service.

**Monetization model:** per-listing fee, SaaS subscription, or revenue share.

### Lane C: Productized Research and Intelligence

Package recurring research into reports, monitoring services, niche data
products, or decision-support subscriptions.

**Monetization model:** monthly subscriptions, premium reports, or consulting
upsells.

## Activation Criteria

A lane can enter build mode only after:

1. the scoring instrument returns `PASS`,
2. required data sources are documented,
3. the journal records the rationale and risks,
4. the first offer and target buyer are stated clearly.

## Operating Loop

1. Intake mission ideas in `docs/strategy/incoming.md`.
2. Score them with `instruments/strategy/score.sh`.
3. Promote the best compliant lane into a scoped experiment.
4. Record outcomes in the mission journal.
5. Feed learnings into the improvement backlog.

## Initial Priorities

1. Stand up the compliance and scoring layer.
2. Validate the Inbox-to-CRM lane on strictly first-party workflows.
3. Keep Autonomous Listing as a parallel hedge because the repo already
   contains a strong blueprint and scaffold.
4. Treat research subscriptions and info products as lower-friction fallback
   monetization if operational services stall.

## Core Success Metrics

- Number of lanes scored and compliance-cleared
- Number of launches shipped to sandbox or pilot
- Pilot revenue or signed intent from compliant offers
- Gross margin potential after automation
- Human review minutes required per delivery cycle
- Number of compliance incidents: target `0`

## Roles

- **Apex Orchestrator:** selects priorities and approves pivots.
- **Portfolio Navigator:** compares expected ROI and autonomy potential across
  lanes.
- **Compliance Guardian:** blocks non-consensual or privacy-invasive models.
- **Telemetry Sentinel:** captures evidence on cost, throughput, and quality.

## First Build Sequence

1. Draft compliant intake and scoring artifacts.
2. Define the Inbox-to-CRM service offer and sandbox workflow.
3. Review Autonomous Listing scaffold for fastest path to monetizable MVP.
4. Capture pricing hypotheses and launch experiments in the journal.
