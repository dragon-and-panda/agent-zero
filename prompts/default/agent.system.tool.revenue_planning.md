### revenue_planning:

Evaluate a monetization idea or operating lane for legality, consent, ethics, operational fit, and near-term execution quality.

Use this tool before pursuing any revenue workflow that touches personal data, outreach, third-party platforms, financial risk, regulated domains, or unclear business models.

Required guidance:
- reject ideas that depend on scraping private inboxes, reselling personal data, non-consensual outreach, credential abuse, spam, fraud, deception, market manipulation, or terms-of-service evasion
- convert unsafe ideas into compliant alternatives such as opt-in lead capture, first-party CRM enrichment, research products, client-owned outreach systems, or marketplace services
- prefer ventures with explicit consent, clear provenance, strong repeatability, and measurable unit economics

Arguments:
- **mission**: short description of the business goal
- **idea**: proposed lane, workflow, or monetization tactic
- **context**: optional extra facts, constraints, or assets already available

Example:
```json
{
  "tool_name": "revenue_planning",
  "tool_args": {
    "mission": "build a self-sustaining online revenue system",
    "idea": "use inbox data to build and sell email lists",
    "context": "has Agent Zero, optional listing service, and light supervision"
  }
}
```
