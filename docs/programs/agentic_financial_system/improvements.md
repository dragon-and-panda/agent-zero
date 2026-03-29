# Agentic Financial System Improvement Backlog

## High Priority

1. **Inbox-to-CRM service scaffold**
   - Add a small service that accepts client-authorized mailbox exports or OAuth tokens.
   - Normalize contacts, companies, consent markers, and message classifications.
   - Output a review queue before any outbound workflow is enabled.

2. **Consent-aware RAG pack**
   - Create a dedicated `knowledge/custom/main/compliance/` area for privacy law, anti-spam summaries, and vendor-specific inbox policies.
   - Inject these references into prompts for any inbox-touching workflow.

3. **Opportunity scoring automation**
   - Extend `instruments/strategy/score.sh` to emit machine-readable JSON for downstream schedulers.
   - Add examples for GO, HOLD, and REJECT cases.

## Medium Priority

4. **Autonomous listing telemetry**
   - Connect listing-service KPIs back to the financial-system mission diary.
   - Track conversion, response latency, refund rate, and operator intervention rate.

5. **Offer generation library**
   - Build reusable proposal templates for compliant service offerings:
     - inbox cleanup,
     - listing optimization,
     - market research briefs,
     - analytics subscriptions.

6. **Reserve-policy dashboard**
   - Define cash reserve thresholds before any speculative lane is activated.
   - Track drawdown, runway, and monthly recurring revenue coverage.

## Low Priority

7. **Sandbox evaluator**
   - Simulate buyer, client, and compliance-review interactions to test workflows before production use.

8. **Partner directory**
   - Catalog lawful data partners, fulfillment vendors, and distribution channels with usage constraints and economics.
