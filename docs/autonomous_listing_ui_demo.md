# Autonomous Listing UI – Visual Demo Brief

This brief describes the visual layout, component inventory, and interaction flow for the seller-facing interface. It can be handed to design/Front-End teams (or a design tool like Figma) to create click-through comps or interactive demos.

---

## 1. Screen Map

1. **Mission Control Dashboard (Live Agent Command Center)**
   - Status strip (Processing → Drafting → Live) with animated progress bar tied to orchestrator telemetry.
   - Agent ticker showing which persona is active (“Vision Stylist enhancing photos…”) with avatar + model badge.
   - KPI cards: views, inquiries, conversion probability, negotiation guardrail meter.
   - “Launch Collaboration Room” button linking to the Zoom-like multi-agent space, with unread indicator if agents are already meeting.
2. **Listing Composer**
   - Left rail: asset gallery with before/after toggle, enhancement presets.
   - Center canvas: AI-generated description + pricing suggestions with inline edit controls.
   - Right rail: marketplace checklist showing publication state per platform.
3. **Engagement Hub**
   - Contact list grouped by platform.
   - Conversation thread with color-coded messages (buyer, seller, AI).
   - Reply composer showing AI suggestions, guardrail warnings, and quick actions (counteroffer, share payment link).

---

## 2. Component Inventory

| Component | Description | Notes |
| --- | --- | --- |
| Hero Progress Bar | Animated gradient with milestone dots | Mirrors state machine from orchestrator |
| KPI Cards | Small panels for Views, Offers, Live Platforms, Telemetry alerts | Include sparkline trend |
| Asset Carousel | Swipeable gallery; hover reveals enhancement details | Hooked to vision pipeline metadata |
| Description Editor | Markdown-esque block with AI suggestions in sidebar | Accept/modify/per-platform tone toggles |
| Marketplace Status Grid | Tiles for Craigslist, Mercari, Nextdoor, OfferUp | Display reference IDs, error badges |
| Conversation Thread | Speech bubbles with avatars (seller, AI agent, buyer) | Each message logs to engagement transcript |
| Reply Composer | Input + AI suggestion chips | Includes guardrail meter + send/approve buttons |

---

## 3. Interaction Flow (Demo Script)

1. **Upload & Preview**
   - Seller drags photos → asset carousel populates with “Enhancing…” overlays.
   - Toast shows “Vision Stylist cleaning backgrounds” with telemetry icon.
2. **Copy Review**
   - Description panel animates with typing effect from Copywriter agent.
   - Seller toggles tone (Premium ↔ Playful) to see instant LLM refresh.
3. **Marketplace Launch**
   - Seller hits “Publish”; marketplace tiles update (Craigslist = Pending, Mercari = Live with ID link).
   - Status strip advances to “Live on 2 platforms.”
4. **Engagement**
   - Buyer ping appears in contact list; thread view opens with message and AI-suggested reply.
   - Seller approves AI reply → timeline shows “Auto-Reply sent by Buyer Liaison.”
5. **Collab Room**
   - Seller clicks “Launch Collaboration Room” to open Zoom-like session with agents, mirroring Section 12 of the main doc.

---

## 4. Live Agent Command Center Notes

- **Agent Presence Strip:** Horizontal ticker with looping avatars; highlight the active agent, fade completed steps, and allow hover to reveal quick summaries (“Copywriter drafted premium copy in 4.2s”).
- **Telemetry Sparklines:** Each agent chip shows latency + cost sparklines pulled from telemetry logs to reinforce transparency.
- **Narrative Toasts:** Floating toasts narrate actions (“Portfolio Navigator approved price ladder”).
- **Marketplace Radar:** Polar chart visualizing readiness per platform (assets, copy, compliance) so sellers can spot blockers instantly.
- **Quick Actions:** “Ask Agent” opens inline chat with selected persona; “Summon All” jumps into the collaboration room.

---

## 5. Asset & Tool Requirements

- **Design System:** Extend existing mission control palette; include dark + light variants.
- **Iconography:** Platform logos, AI agent avatars, guardrail meter, telemetry bell.
- **Motion:** Micro-animations for progress bar, typing indicator, card entrance.
- **Prototyping Tool:** Figma or Penpot with interactive components for the above flow.
- **Demo Data:** Sample listing (e.g., “Mid-century walnut table”), mock metrics, transcript snippets from mission diary.

This brief provides enough fidelity for the design team to deliver a visual demo that mirrors the live agent workflow.
