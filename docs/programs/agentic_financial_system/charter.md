# Agentic Financial System Charter

## Mission

Build a durable, low-touch revenue system using Agent Zero that improves its own operating playbooks over time while staying inside legal, ethical, and platform-compliant boundaries.

## Why This Charter Exists

The incoming mission included a request to extract email addresses from Gmail and other files, organize them, and sell the resulting lists. That path is rejected. This program replaces it with monetization lanes that preserve consent, privacy, and auditability.

See `docs/policies/compliance_pack.md` for the non-negotiable guardrails.

## Approved Revenue Lanes

### Lane 1: Inbox-to-CRM Operator

Use first-party Gmail access only for the mailbox owner's operational benefit:

- summarize inbound leads and customer conversations,
- tag conversations by intent, urgency, and stage,
- extract company and deal context into a client-owned CRM,
- draft follow-ups for human review or approved auto-send rules,
- surface opt-in or warm inbound contacts already associated with the business.

Explicit non-goal: exporting or reselling addresses as a marketable list.

### Lane 2: Autonomous Listing Service

Use the existing blueprint in `docs/autonomous_listing_service.md` to generate revenue from listing creation, cross-posting, negotiation support, and seller operations.

### Lane 3: Research and Intelligence Products

Package public, non-personal information into reports, watchlists, templates, and niche research subscriptions. Revenue comes from analysis quality, not contact resale.

### Lane 4: Affiliate and Content Engine

Create comparison pages, tutorials, niche media, and tool recommendations that monetize through affiliate links, sponsorships, or productized services.

## Operating Principles

1. **Consent first:** personal data is processed only for the owner or an authorized client.
2. **Tools are generated on demand:** build small instruments for scoring, routing, and reporting instead of hard-coding brittle flows.
3. **Revenue quality beats speed:** durable, repeatable lanes outrank quick but risky shortcuts.
4. **Every lane is scored:** no lane goes live until legality, consent, provenance, and terms checks pass.
5. **Logs over lore:** decisions and outcomes are written to mission journals so future cron runs inherit context.

## Recommended Initial Build Order

1. Stand up the scoring gate in `instruments/strategy/score.sh`.
2. Launch a narrow Inbox-to-CRM prototype for first-party mailboxes.
3. Run the Autonomous Listing Service as the main productized revenue lane.
4. Add a research-product lane to diversify cash flow and reduce marketplace dependence.

## Data and RAG Policy

RAG over Gmail is allowed only for first-party productivity workflows where the mailbox owner or authorized operator benefits directly. Valid uses include summarization, semantic retrieval, support triage, and CRM drafting.

RAG is not permitted for:

- collecting third-party contacts for sale,
- building cold-outreach inventories,
- packaging inbox-derived addresses into a transferable asset.

## Orange DataScaping Role

Orange DataScaping can serve as a visual workspace for:

- clustering inbound conversations,
- segmenting opt-in contacts,
- analyzing support categories,
- organizing approved first-party CRM exports.

It cannot be used as a staging tool for personal-data brokerage.

## Activation Criteria

A lane may be activated only if:

- the scoring instrument returns `PASS`,
- the lane has a written operating procedure,
- the data provenance is documented,
- a rollback or shutdown path exists.

## Success Measures

Track the following across lanes:

- monthly recurring revenue or monthly gross profit,
- percentage of work executed autonomously,
- lead or order cycle time,
- customer satisfaction or response quality,
- compliance incidents, with a target of zero.
