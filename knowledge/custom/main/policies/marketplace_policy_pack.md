# Marketplace Policy Pack

Use this reference before generating copy, pricing guidance, or publishing listings. Each rule should be cited in mission diaries when a decision relies on it.

## Universal Guardrails
- Only describe items you have authority to sell; never list prohibited goods (weapons, counterfeit items, recalled electronics, medical devices).
- No discriminatory language, harassment, or personal data beyond what is necessary to complete the transaction.
- All claims about condition, provenance, or performance must be verifiable via user-provided evidence (photos, receipts) or explicitly marked as "untested".
- Always include pickup/delivery expectations, payment methods, and response-time commitments in plain language.
- If taxes, platform fees, or shipping costs apply, disclose them before collecting payment info.

## Image & Media Standards
1. Remove EXIF/location metadata before publishing.
2. Show the actual item (no stock imagery unless explicitly labeled) and include:
   - One hero shot (front/primary view)
   - Detail shot (defects, unique features)
   - Context shot (scale or usage scenario)
3. Do not watermark third-party logos or copyrighted elements unless you own the rights.
4. Apply tasteful enhancements only (exposure, color balance, background cleanup). Never alter the item to misrepresent condition.

## Platform-Specific Requirements

### Craigslist
- **Tone:** Informational and concise; no emoji or ALL CAPS headlines.
- **Contact Info:** Use anonymized Craigslist relay email; never paste personal phone numbers unless the seller explicitly opts in.
- **Links:** External links allowed only when they reference manuals or proof-of-purchase; no tracking pixels.
- **Pricing:** Single currency (USD) with clear negotiable status ("firm", "obo", "trade").
- **Renewals:** Wait 48h before reposting similar content to avoid ghosting.

### Mercari
- **Photos:** Minimum 3 images; first must show the full item on a clean background.
- **Shipping:** Select one of Mercari's prepaid options or "Local Pickup". Include package weight/size estimates for automated label creation.
- **Prohibited Copy:** No off-platform contact instructions, no "cash only" statements, no personal payment handles.
- **Condition Tags:** Must use Mercari's canonical states ("New", "Like New", "Good", "Fair", "Poor"). Provide defect notes if not "New".
- **Returns:** Default is "No returns" unless seller explicitly offers them. If returns are allowed, specify time window.

### Nextdoor
- **Community Fit:** Reference neighborhood value ("great for home office", "fits small apartment") to boost trust.
- **Safety:** Encourage in-person exchange at public locations or porch pickup. Never suggest entering private homes without vetting.
- **Messaging:** Keep responses friendly and neighborly; avoid aggressive price haggling language.
- **Listings Lifespan:** Auto-archived after 30 days; refresh plan should be logged in mission diary.
- **Prohibited Content:** No political merchandise, services requiring licensing (contracting, childcare) unless credentials are provided.

## Pricing & Offer Compliance
- Use telemetry data or recent comps before suggesting price cuts. Document the source (market dataset, competitor listing, etc.).
- Price floors: never accept offers below 60% of anchor price unless seller explicitly authorizes or inventory has been active >30 days.
- When buyer proposes barter or payment plan, involve the human seller for approval and capture decision in memory.

## Messaging & Negotiation Guardrails
- Always disclose enhanced media ("background cleaned", "colors balanced") in the transcript summary.
- If buyer requests policy-violating action (shipping to banned region, paying outside platform), politely decline and note incident for Risk Governor.
- Keep a neutral, professional tone even when buyer is informal. Empathy is welcome; promises must be actionable.

## Shutdown Protocol
- When sale completes, immediately:
  1. Confirm buyer receipt and satisfaction message draft.
  2. Close or pause all duplicate listings to avoid double-selling.
  3. Write a memory entry tagged `sale:<item_id>` summarizing platform, final price, fees, and learnings.
- Archive artifacts (final copy, media, negotiation log) under mission storage for future fine-tuning or case studies.
