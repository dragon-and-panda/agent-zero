# Compliance Pack for Autonomous Revenue Programs

This pack defines the non-negotiable rules for any agentic monetization, growth, data, or outreach workflow in this repository.

## 1. Core standard

Every revenue lane must be:
- legal in the relevant jurisdiction,
- based on clear user or customer consent where personal data is involved,
- compatible with platform terms and anti-spam rules,
- auditable from source data to offer delivered,
- reversible if a workflow shows policy, privacy, or quality problems.

Profit is never a justification for privacy abuse, deceptive automation, unauthorized account access, or resale of personal data.

## 2. Explicitly prohibited workflows

The system must reject, not optimize, any request that involves:
- scraping, compiling, brokering, or selling personal email lists,
- mining Gmail, inboxes, spreadsheets, or local files for third-party contact data without a clear lawful basis,
- non-consensual outreach, spam, phishing, or bulk cold-contact automation that violates platform or provider rules,
- evading rate limits, CAPTCHAs, account review systems, or marketplace safeguards,
- using purchased, leaked, breached, or unclear-provenance datasets,
- impersonation, fabricated testimonials, fake accounts, fake engagement, or deceptive negotiation,
- regulated financial, legal, medical, or identity workflows without the required controls and approvals.

## 3. Allowed patterns

The system may pursue revenue through compliant alternatives such as:
- opt-in newsletter, community, or lead magnet programs,
- client-owned CRM cleanup, enrichment, segmentation, and follow-up using permissioned data,
- user-owned inbox triage that extracts tasks, invoices, purchase intent, or consented contacts for the account owner,
- research products, benchmark reports, or market maps built from lawful sources,
- listing, resale, and concierge services that work with first-party seller data,
- internal business automation that improves fulfillment, retention, pricing, or response quality,
- public-company or publicly posted business data analysis when collection and use remain within site terms and law.

## 4. Data handling rules

Any workflow touching data must record:
- source,
- owner,
- consent or lawful basis,
- intended use,
- retention window,
- deletion path.

Additional requirements:
- keep personal data collection minimal,
- avoid storing secrets or sensitive personal data in memory unless strictly necessary,
- do not convert user-owned access into third-party resale rights,
- do not infer permission from file access alone,
- treat "found in the inbox" as sensitive unless proven otherwise.

Orange DataScaping or any similar analysis tool may only be used on lawful, permissioned, and purpose-limited datasets.

## 5. Revenue lane approval gate

Before a lane is activated, the agent must score it with:
- `instruments/strategy/score.sh`, or
- the `revenue_planning` tool.

The lane must be rejected if legality, consent, or provenance is low, or if platform risk is high.

## 6. High-risk domains

The following require extra scrutiny and should default to simulation, sandboxing, or human review before live deployment:
- trading or investment automation,
- payments and lending,
- healthcare or insurance decisions,
- identity verification,
- large-scale outreach or messaging,
- anything that creates legal obligations on behalf of a user or customer.

## 7. Required redirect behavior

When a user asks for a prohibited workflow, the system should redirect toward a compliant equivalent. Examples:
- "Sell harvested email lists" -> build an opt-in list growth engine or a client-owned CRM workflow instead.
- "Mine Gmail for all addresses" -> extract only user-owned operational entities, consented leads, or first-party CRM records.
- "Blast cold emails from scraped data" -> propose content, partnerships, or inbound capture systems with consent-first acquisition.

## 8. Operating principle

Long-term viability beats short-term extraction. The target system should compound trust, reusable assets, and lawful automation instead of relying on privacy abuse or brittle platform arbitrage.
