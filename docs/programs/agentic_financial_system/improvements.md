# Agentic Financial System Improvement Backlog

## Priority Backlog

### 1. Build the intake-to-score loop
- Create a repeatable workflow for adding opportunities to `docs/strategy/incoming.md`.
- Require every lane to include customer, data source, consent model, and pricing hypothesis.
- Auto-run the scoring instrument before any implementation work begins.

### 2. Turn inbox-to-CRM into a narrow offer
- Choose one vertical with high inbox load and clear ROI.
- Define the first MVP workflow:
  - message classification
  - summary generation
  - CRM update
  - suggested reply
- Package it as a fixed-scope service plus retainer.

### 3. Operationalize the listing service blueprint
- Convert the listing blueprint into a scoped MVP.
- Identify the first supported marketplaces and a lightweight seller workflow.
- Define KPI targets for conversion uplift, response time, and close rate.

### 4. Create a reusable compliance review step
- Add a checklist that runs before launch for legality, consent, provenance, and platform-risk review.
- Record rejection reasons so the system learns which lanes to avoid.

### 5. Add basic financial telemetry
- Track revenue, gross margin, automation coverage, and failure rate per lane.
- Keep the first dashboard simple and auditable.

### 6. Build offer templates
- Write standardized discovery, onboarding, pricing, and renewal templates.
- Reduce custom work so each successful lane is easier to sell repeatedly.

### 7. Productize a research lane
- Pick one vertical where ongoing monitoring has clear buyer value.
- Define a recurring output format and delivery cadence.
- Validate whether subscriptions or custom retainers convert better.

## Parking Lot

- broader multi-tenant SaaS packaging before a service lane proves demand
- high-risk outreach automation
- any data acquisition path that relies on scraping personal contact data
