# SOP: Listing Concierge Workflow

Structured procedure for the Listing Publisher persona and subordinate agents. Follow sequentially; document deviations in mission diary.

## Phase 1: Intake & Validation
1. **Collect Inputs:** seller intent, target price range, required platforms, raw description, and image bundle.
2. **Screen Assets:** run policy pack checklist (prohibited items, missing disclosures). Request clarifications before proceeding.
3. **Create Mission Entry:** log mission ID, item name, priority, due date in `docs/programs/autonomous_listing/journal.md` and memory.

## Phase 2: Media Enhancement
1. Run Vision Enhancer instrument on each photo:
   - Background cleanup
   - Exposure + color correction
   - Smart crop for hero/detail/context shots
2. Generate thumbnails sized per marketplace requirements (Craigslist 600x450, Mercari 1080x1080, Nextdoor 1200px long edge).
3. Record transformation metadata (operations, tools, hashes) in mission diary for audit.

## Phase 3: Narrative & Pricing
1. Query `knowledge/custom/main/policies/marketplace_policy_pack.md` + voice guide for tone constraints.
2. Use description generator pipeline with inputs:
   - Item facts
   - Target persona (family, collector, remote worker, etc.)
   - Sentiment dial (premium, friendly, urgency)
3. Run pricing heuristic:
   - Pull comparable listings or seller-provided MSRP
   - Apply condition multipliers (New 1.0, Like New 0.85, Good 0.7, Fair 0.55)
   - Suggest anchor price + "fair offer" range and cite data source
4. Persist the narrative draft + pricing rationale to memory before syndication.

## Phase 4: Compliance & QA
1. Re-run policy checklist per platform. Confirm:
   - Required disclosures present
   - Shipping/payment statements included
   - Marketplace-specific wording used (condition tags, tone)
2. Summarize QA results (pass/fail, notes) and attach to mission diary.

## Phase 5: Publishing & Telemetry
1. Invoke marketplace adapter instrument per platform with payload:
   - Enhanced media URLs
   - Long + short copy
   - Pricing bundle
   - Contact preferences
2. Capture publication IDs/links and push to telemetry (`logs/reports/<week>.md`).
3. Update seller dashboard state to "Live" with timestamps.

## Phase 6: Engagement Management
1. Route inbound inquiries to Engagement Hub.
2. Use buyer liaison script to answer FAQs, negotiate within guardrails, and request approvals when necessary.
3. Tag each conversation with sentiment + status for Telemetry Sentinel.

## Phase 7: Closure
1. When sale confirmed, trigger shutdown protocol:
   - Confirm payment/shipping outcome
   - Close remaining listings
   - Archive conversation logs
2. Capture final metrics: time-to-first-offer, accepted price delta, image performance (CTR if available).
3. Write retrospective snippet to mission diary + knowledge base if insights are reusable.

**Reminder:** Every phase should end with a memory entry referencing the mission ID so other agents (Portfolio Navigator, Telemetry Sentinel) can trace the state without re-running tools.
