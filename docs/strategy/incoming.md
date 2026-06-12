# Strategy Intake Queue

Use this queue for monetization ideas before they become active missions.

## Intake Format

For each opportunity, record:

1. **Name**
2. **Customer**
3. **Offer**
4. **Data required**
5. **Consent / provenance**
6. **Why now**
7. **Expected margin**
8. **Repeatability**
9. **Automation fit**
10. **Main compliance risks**

## Active Intake Candidates

### 1. Inbox-to-CRM Triage for First-Party Sales Teams
- **Customer:** Businesses that already own the inbox and customer relationship.
- **Offer:** Classify inbound messages, extract structured deal data, and draft follow-ups inside the customer's own systems.
- **Data required:** Customer-provided email or CRM data only.
- **Consent / provenance:** First-party business records under operator control.
- **Why now:** High manual workload, clear operational ROI, and fits Agent Zero's automation model.
- **Expected margin:** Medium to high if sold as retained workflow automation.
- **Repeatability:** High across verticals with the same intake pipeline.
- **Automation fit:** High.
- **Main compliance risks:** Must maintain documented authorization, least privilege, and retention controls.

### 2. Autonomous Listing Concierge
- **Customer:** Individuals or small businesses selling inventory.
- **Offer:** Transform photos and notes into polished listings, pricing guidance, and managed inbox replies.
- **Data required:** User-supplied listing assets and platform account access with permission.
- **Consent / provenance:** First-party by default.
- **Why now:** Already aligned with `docs/autonomous_listing_service.md`.
- **Expected margin:** Medium, potentially high with managed service packaging.
- **Repeatability:** High by category and platform.
- **Automation fit:** High.
- **Main compliance risks:** Marketplace policy compliance and messaging guardrails.

### 3. Public-Data Research Briefs
- **Customer:** Operators who need niche market intelligence.
- **Offer:** Curated reports from public, licensed, or customer-supplied datasets.
- **Data required:** Public web sources, licensed data, internal customer data where permitted.
- **Consent / provenance:** Clear if source licensing is documented.
- **Why now:** Fast path to cash with minimal platform integration overhead.
- **Expected margin:** Medium.
- **Repeatability:** Medium.
- **Automation fit:** Medium to high.
- **Main compliance risks:** Citation quality, source licensing, and avoiding personal-data misuse.

## Explicitly Rejected Requests

The following category is permanently rejected and should not be re-queued:

- Harvesting Gmail or other mailbox contents to compile and sell personal email address lists.
