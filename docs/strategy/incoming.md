# Strategy Intake Queue

Use this page as the durable intake queue for new revenue lanes, experiments, and mission pivots.

## Triage rubric

For each new idea, capture:
- objective,
- customer,
- asset or data source,
- consent and provenance status,
- platform dependencies,
- expected unit economics,
- automation feasibility,
- risks and blockers,
- next validation step.

Every idea should be scored with `instruments/strategy/score.sh` or the `revenue_planning` tool before activation.

## Current queue

### 1. Inbox-to-CRM operator
- Objective: Turn a user's own inbox and approved files into a structured CRM, follow-up queue, and opportunity tracker.
- Status: active candidate
- Notes: Allowed only for first-party or client-authorized data; never for contact resale or third-party harvesting.

### 2. Autonomous listing concierge
- Objective: Convert seller photos and notes into premium marketplace listings and buyer-response workflows.
- Status: active hedge
- Notes: Reuse `docs/autonomous_listing_service.md` as the technical blueprint and keep platform rules explicit.

### 3. Research product factory
- Objective: Produce benchmark reports, market maps, and operational intelligence products from lawful sources.
- Status: active hedge
- Notes: Strong fit for repeatable content and workflow automation with low personal-data exposure.

## Rejected examples

### Personal email list brokerage
- Objective: scrape or collect email addresses from inboxes, files, or other sources and sell the compiled lists.
- Status: rejected
- Reason: fails legality, consent, provenance, and anti-spam checks in the compliance pack.
- Redirect: build an opt-in acquisition engine, a client-owned CRM workflow, or a research product instead.
