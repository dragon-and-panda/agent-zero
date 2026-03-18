# Strategy Intake Queue

Use this file to classify incoming opportunities before work starts. Pair it with `instruments/strategy/score.sh` for a quick GO/HOLD/REJECT pass.

## Current Intake Decisions

| Status | Opportunity | Why | Next move |
| --- | --- | --- | --- |
| REJECT | Harvest email addresses from received/sent/CC data and sell the list | Violates consent, privacy, and anti-spam boundaries; blocked by `docs/policies/compliance_pack.md` | Do not implement |
| HOLD | Deploy operating capital into Forex as an early revenue engine | High downside risk, weak reversibility, and no validated edge yet | Revisit only after reserves, written risk controls, and paper-trading evidence |
| GO | Consent-based Inbox-to-CRM Hygiene Service | Customer-owned data, direct value, repeatable workflow, low capital needs | Package as a scoped service with explicit authorization and deletion policy |
| GO | Autonomous Listing / Resale Concierge | Matches existing repo direction, monetizes operational automation, and can produce case studies | Continue building product and service delivery assets |
| GO | Tutorial, playbook, and YouTube-style documentation product | Creates reusable content assets and inbound demand | Record the build process and turn it into a course plus video scripts |
| GO | Public-data research and lead qualification for opted-in prospects | Can support consulting and outreach without private-data abuse | Limit sources to public/business data and compliant outreach channels |

## Intake Template

Copy this block for new ideas:

```md
### Opportunity
- Summary:
- Customer:
- Revenue model:
- Data used:
- Consent path:
- Dependencies:
- Fastest test:
- Failure mode:
- Redundancy / fallback:
- Initial classification: GO / HOLD / REJECT
```

## Review Notes

- Prefer opportunities that can be sold as a service first, then standardized into a product.
- Prefer workflows that create reusable assets: SOPs, prompts, case studies, templates, or datasets that do not contain sensitive personal information.
- Reject any opportunity whose business model depends on data resale instead of customer value delivery.
