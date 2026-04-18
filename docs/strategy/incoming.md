# Strategy Intake Queue

This queue is the canonical intake surface for new autonomous venture ideas.
Every entry must include consent, legality, provenance, platform-policy, and
economics checks before an agent can activate execution.

## Intake Template

```md
### Mission
- Summary:
- Customer:
- Revenue model:
- Inputs/data sources:
- Consent status:
- Data provenance:
- Platform/TOS considerations:
- Legal/regulatory notes:
- Why this is valuable:
- Next action:
```

## Active Queue

### Mission
- Summary: Build an opt-in inbox-to-CRM workflow for small businesses that
  triages inbound messages, drafts replies, and captures leads only when the
  customer has directly contacted the business.
- Customer: Solo operators and local service businesses.
- Revenue model: Monthly SaaS subscription plus setup fee.
- Inputs/data sources: Business-owned inboxes, submitted forms, and customer
  messages with explicit business relationship context.
- Consent status: Pass. Uses first-party communications and customer-initiated
  messages.
- Data provenance: Pass. Data is sourced from the business that owns the inbox
  and customer relationship.
- Platform/TOS considerations: Must respect mailbox provider rules, rate limits,
  privacy policies, and avoid unauthorized scraping.
- Legal/regulatory notes: Requires retention, consent logging, and deletion
  workflows.
- Why this is valuable: Fast path to revenue with repeatable operational value.
- Next action: Score with `instruments/strategy/score.sh`, then prototype the
  first response and CRM handoff loop.

### Mission
- Summary: Expand the Autonomous Listing Service into a sellable concierge for
  lawful marketplace listing creation and seller support.
- Customer: Individuals and small resellers who want better listings and inbox
  management.
- Revenue model: Per-listing fee, subscription, or concierge upsell.
- Inputs/data sources: Seller-provided photos, notes, preferences, and
  marketplace policy summaries.
- Consent status: Pass. Seller-owned assets only.
- Data provenance: Pass. Inputs come from the seller or lawful public guidance.
- Platform/TOS considerations: Channel-specific compliance and rate limits must
  be enforced.
- Legal/regulatory notes: Must avoid deceptive listings and preserve required
  disclosures.
- Why this is valuable: Adjacent to existing repo assets and technically
  aligned with the current microservice scaffold.
- Next action: Add mission metrics and compliance hooks before live automation.

## Rejected Example

### Mission
- Summary: Compile and sell personal email address lists from inboxes or other
  files to third parties.
- Customer: None approved.
- Revenue model: Contact-data brokerage.
- Inputs/data sources: Email accounts, message bodies, attachments, or scraped
  files containing personal contact data.
- Consent status: Fail. No verified opt-in for resale.
- Data provenance: Fail. Source ownership and downstream rights are unclear.
- Platform/TOS considerations: Likely violates provider terms and anti-spam
  rules.
- Legal/regulatory notes: High risk under privacy, consumer protection, and
  anti-spam regimes.
- Why this is valuable: Not acceptable.
- Next action: Reject and replace with opt-in lead generation, first-party CRM
  automation, or digital-product monetization.
