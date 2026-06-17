# Strategy Intake Queue

## Intake rules
- Every mission must document the offer, customer, delivery path, legality, consent model, and platform dependencies before execution.
- Any mission involving scraping, inbox access, personal-contact brokerage, spam, credential harvesting, or resale of personal data is rejected at intake.
- Approved missions must start with a small, testable lane and a measurable success metric.

## Queue

### Candidate: Opt-in inbox-to-CRM assistant
- Status: active
- Goal: help a user process their own opted-in business inbox into structured CRM actions, drafts, and summaries.
- Delivery path: local mailbox connectors or exported user-owned data only, with explicit per-account authorization.
- Revenue model: subscription or managed-service fee.
- Risks to monitor: account-scoping mistakes, retention policy drift, and outbound messaging policy violations.

### Candidate: Autonomous listing optimization service
- Status: active hedge
- Goal: improve lawful marketplace listings through image cleanup, copy generation, repricing suggestions, and response drafting.
- Delivery path: user-owned inventory, platform-approved access, and transparent audit logs.
- Revenue model: service fee or usage-based pricing.
- Risks to monitor: platform API limits, misleading claims in listing copy, and unsupported automation flows.

### Candidate: Research digest for regulated operators
- Status: active hedge
- Goal: sell curated research briefings, workflow templates, and compliance-aware playbooks to operators in narrow niches.
- Delivery path: first-party research, licensed sources, and analyst review.
- Revenue model: subscription, sponsorship, or bespoke reports.
- Risks to monitor: source licensing, factual drift, and sector-specific compliance needs.

### Rejected: resell compiled email lists from scraped or mailbox-derived data
- Status: rejected
- Reason: fails consent, provenance, privacy, and anti-spam requirements and creates legal and platform-policy exposure.
