# Agentic Financial System Improvement Backlog

## Highest Priority

1. **Inbox-to-CRM schema**
   - Define a canonical record for mailbox-derived opportunities.
   - Include provenance, consent status, thread URL/ID, next action, owner, and allowed use.

2. **Mission scoring in the operating loop**
   - Ensure new lanes are scored before they enter implementation.
   - Persist PASS/HOLD/REJECT decisions with rationale.

3. **Gmail RAG workflow design**
   - Define safe retrieval scopes.
   - Limit outputs to summaries, relationship context, and internal follow-up suggestions.

4. **Orange analysis template**
   - Create a repeatable Orange workflow for first-party segmentation and opportunity scoring.
   - Include data minimization and masking guidance.

## Medium Priority

5. **Revenue telemetry**
   - Track activation rate, follow-up completion, subscriber growth, recurring revenue, and profit by lane.

6. **Offer library**
   - Create productized offers for research briefs, CRM cleanup, inbox triage, and workflow automation.

7. **Consent-aware CRM enrichment**
   - Add rules so contacts without clear provenance or allowed-use metadata remain blocked from activation.

## Explicitly Rejected Ideas

- email list brokerage;
- inbox harvesting for unsolicited outreach;
- scraped-contact resale businesses;
- any workflow that depends on Terms-of-Service evasion.
