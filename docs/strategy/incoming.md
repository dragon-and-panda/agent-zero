# Incoming Opportunity Queue

This file is the intake queue referenced by the super-agency blueprint. Each row is a candidate revenue track scored by `instruments/strategy/score.sh`.

Scoring fields use a 1-5 scale where higher is better except `effort`, `risk`, and `capital_required`, where lower is better.

| id | opportunity | compliance | automation_fit | speed_to_revenue | effort | risk | capital_required | redundancy | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inbox_crm_hygiene | Consent-based inbox-to-CRM hygiene service for sponsor-owned mailboxes | GO | 5 | 4 | 2 | 1 | 1 | 4 | Use RAG on authorized email exports to classify contacts, threads, and follow-up tasks; export only opted-in or business-relationship contacts into a sponsor CRM. |
| autonomous_listing_service | AI-assisted listing creation and resale operations for owned inventory | GO | 4 | 4 | 3 | 2 | 2 | 5 | Reuse the existing listing service docs and code paths for a fast path to cash generation. |
| ops_playbook_course | Turn operating procedures and lessons learned into a course, templates, and YouTube-ready narrative assets | GO | 4 | 3 | 2 | 1 | 1 | 4 | Productize the mission journal, SOPs, and demo assets after they have proven value in real operations. |
| smb_ai_ops_retainers | Small-business AI operations setup, reporting automation, and document workflows | GO | 3 | 4 | 3 | 2 | 1 | 5 | Sell setup plus recurring retainers; keep scope narrow and reuse templates aggressively. |
| regulated_trading_lab | Paper-traded strategy research with strict risk gates before any real capital | HOLD | 2 | 1 | 4 | 5 | 3 | 2 | No live deployment until reserve, policy, legal, and sample-size gates are satisfied. |
| personal_email_brokerage | Compile addresses from received, sent, and CC mail for resale | REJECT | 4 | 3 | 2 | 5 | 1 | 1 | Rejected by compliance pack because it depends on privacy invasion, non-consensual reuse, and likely anti-spam violations. |
