# Contractor Client Hub (AI + Web3 Escrow MVP)

This service provides an MVP for:
- AI-assisted contract drafting in a shared client/contractor thread,
- meeting-session workflow for video chat orchestration with a neutral AI avatar,
- backend-issued meeting join tokens for WebRTC room access,
- contractor bid intake (pre-chat uploads or in-meeting submission),
- line-item deliverables with explicit expectations for both parties,
- documentation instructions (`before`, `during`, `after`) per deliverable,
- evidence submissions + automated AI review,
- AI-generated progress reports and email correspondence drafts,
- provider-backed progress email send attempts + webhook delivery reconciliation,
- remediation addendum flow + dispute/arbitration handling,
- escrow state transitions suitable for USDT smart-contract integration.

It is designed as a practical backend scaffold that can be paired with a web frontend.

---

## 1) Quick Start

```bash
cd services/contractor_client_hub
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Health check:

```bash
curl http://localhost:8010/health
```

---

## 2) Core Workflow

1. `POST /threads`  
   Create a contract thread from intended summary + terms.
2. `POST /threads/{thread_id}/messages`  
   Client/contractor collaborate in chat.
3. `POST /threads/{thread_id}/bids`  
   Contractor uploads templated line-item bid + estimated costs.
4. `POST /threads/{thread_id}/meetings`  
   Create video-room session metadata and launch neutral AI avatar facilitation.
5. `POST /threads/{thread_id}/meetings/{meeting_id}/events`  
   Append live meeting transcript events (client, contractor, AI avatar).
6. `POST /threads/{thread_id}/meetings/{meeting_id}/end`  
   Close session and store transcript summary.
7. `POST /threads/{thread_id}/meetings/{meeting_id}/join-token`  
   Issue signed room token for participant join.
8. `POST /threads/{thread_id}/ai/refresh-scope`  
   AI rebuilds deliverables and evidence plan from thread context.
9. `POST /threads/{thread_id}/progress-reports`  
   Generate structured progress report entries.
10. `POST /threads/{thread_id}/emails/draft`  
   Draft neutral progress correspondence email from report data.
11. `POST /threads/{thread_id}/emails/{email_id}/send`  
   Send drafted email via configured provider (`log` or `relay`).
12. `POST /integrations/email/webhook`  
   Apply delivery/bounce events from provider webhook callbacks.
13. `POST /threads/{thread_id}/emails/{email_id}/sent`  
   Manual sent marker (fallback/audit override).
14. `POST /threads/{thread_id}/acknowledge` (both parties)  
   Scope lock and readiness for escrow funding.
15. `POST /threads/{thread_id}/escrow/fund`  
   Record escrow funding (USDT flow stub with tx metadata).
16. `POST /threads/{thread_id}/deliverables/{deliverable_id}/evidence`  
   Contractor submits evidence artifacts.
17. `POST /threads/{thread_id}/ai/review`  
   AI checks evidence completeness; pass or remediation addendum.
18. `POST /threads/{thread_id}/escrow/release`  
   Disburse contractor/platform split.
19. Optional: `POST /threads/{thread_id}/dispute` and `/arbitrate`.

---

## 3) MCP Server

Run as MCP stdio server:

```bash
cd services/contractor_client_hub
python -m app.mcp_server
```

Includes tools such as:
- `create_contract_thread`
- `add_thread_message`
- `submit_contractor_bid`
- `create_meeting_session`
- `add_meeting_event`
- `issue_meeting_join_token`
- `end_meeting_session`
- `refresh_scope_with_ai`
- `create_progress_report`
- `draft_progress_email`
- `send_progress_email`
- `apply_email_webhook`
- `mark_progress_email_sent`
- `fund_contract_escrow`
- `submit_deliverable_evidence`
- `run_ai_evidence_review`
- `release_escrow`
- `raise_dispute`
- `arbitrate_dispute`

---

## 4) Smart Contract Artifact

Reference Solidity contract:

- `contracts/AIAssistedEscrow.sol`

This contract is a starting point for on-chain escrow, with AI-arbiter-mediated approval and dispute settlement.

---

## 5) Desktop Local Signing UI (Optional)

Local validation/signing desktop client:

- `clients/desktop_escrow_ui.py`

Install extras:

```bash
pip install customtkinter
```

Run:

```bash
python clients/desktop_escrow_ui.py
```

---

## 6) Research Seed Scraper (Optional)

Public listing title seed collector for market-language research:

- `app/services/research_seeds.py`

Use responsibly and comply with target site policies.

---

## 7) Important Notes

- This is an MVP and **not** a full legal/compliance product.
- Smart contracts should be externally audited before production funds.
- AI evidence review should be treated as assistive; retain human oversight for high-stakes jobs.

---

## 8) Key Environment Variables

```bash
# Realtime rooms/tokens
CCH_REALTIME_ROOM_BASE_URL=https://meet.example.com
CCH_REALTIME_TOKEN_SECRET=replace-with-strong-secret
CCH_REALTIME_TOKEN_TTL_SECONDS=3600

# Email delivery
CCH_EMAIL_PROVIDER=log              # log | relay
CCH_EMAIL_FROM_ADDRESS=no-reply@example.com
CCH_EMAIL_RELAY_ENDPOINT=https://mailer.example.com/send
CCH_EMAIL_RELAY_BEARER_TOKEN=...
CCH_EMAIL_WEBHOOK_SECRET=...
```
