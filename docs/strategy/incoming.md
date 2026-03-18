# Incoming Opportunity Queue

Use this file to capture candidate revenue ideas before they enter implementation. Every idea should be scored with `instruments/strategy/score.sh` and checked against `docs/policies/compliance_pack.md`.

| Idea | Status | Why | Notes |
| --- | --- | --- | --- |
| Extract email addresses from received/sent/CC mailboxes and compile lists | REJECT | Requires inbox mining and personal-data extraction outside a bounded, consent-based service model | Violates the compliance pack |
| Sell compiled email lists to online services | REJECT | Personal-data brokerage and spam risk | Automatic reject |
| Use Orange or similar analytics tooling on exported inbox data | REFRAME | Only acceptable when the customer explicitly authorizes a defined cleanup or CRM workflow | Limit scope to customer-owned data |
| Consent-based inbox-to-CRM hygiene service | GO | Solves a real business problem while staying within opt-in service delivery | Candidate Phase 1 offer |
| AI listing concierge for resale and local marketplaces | GO | Productized, automatable, and already aligned with existing repo work | Reuse the autonomous listing service |
| Tutorial/course documenting the build journey | GO | Creates audience, trust, and a sellable digital asset | Pair with a YouTube funnel |
| Anthropomorphic narrator/story IP around the build journey | GO | Useful as a content wrapper and brand differentiator | Keep claims grounded in real progress |
| Forex or other leveraged trading as immediate revenue source | HOLD | High downside and weak fit for an early autonomous business operating system | Restrict to paper trading and research until separate risk controls exist |

---

## Phase 1 Launch Order
1. Consent-based inbox-to-CRM hygiene service
2. AI listing concierge / resale workflow
3. Course + YouTube documentation flywheel
4. Public-data research and affiliate partnerships

## Contingency Logic
- If a service offer underperforms, shift traffic and effort to content and template sales rather than expanding risk.
- If compliance is unclear, pause and reframe the offer instead of testing live.
- If manual workload spikes, productize the most repetitive step before adding more acquisition channels.
