# Improvement Backlog

## Highest Priority

1. Define the first build lane.
   - Preferred candidate: Inbox-to-CRM Hygiene Service using explicit customer authorization.
   - Alternative: extend the Autonomous Listing Service already documented in this repo.

2. Add connector specs.
   - Gmail / Google Workspace OAuth scope boundaries.
   - CRM import/export schemas.
   - audit logging and retention rules.

3. Create a reusable scoring log format.
   - save one scorecard per candidate lane under `docs/strategy/`.

## Medium Priority

4. Add a compliance-aware intake template for new monetization ideas.

5. Build dashboards for:
   - revenue by lane;
   - time-to-cash;
   - compliance incidents;
   - automation cost per deliverable.

6. Add prompt personas for:
   - Growth Studio;
   - Compliance Guardian;
   - Revenue Operator.

## Lower Priority

7. Add sandbox datasets for inbox and listing workflows so future runs can test safely without real customer data.

8. Add a client-facing reporting pack template.
