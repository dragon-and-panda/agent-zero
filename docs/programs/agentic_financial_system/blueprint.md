# Agentic Financial System Blueprint

This blueprint reframes the financial-system mission into a compliant architecture that can run with low human touch.

## 1. System layers

### Command layer

- Apex operator sets goals, budgets, and risk tolerance.
- Every proposed venture is scored before execution.
- Unsafe ideas are redirected into compliant alternatives.

### Knowledge layer

- First-party files and approved documents are imported into knowledge storage.
- Owner-authorized email can be transformed into summaries, entities, and searchable notes.
- Raw mailbox content is not treated as a saleable asset.

### Execution layer

- Agents run research, build landing pages, create offers, and maintain content or automations.
- Instruments capture repetitive checks such as strategy scoring and compliance review.

### Revenue layer

- Focus on offers with recurring value: software, services, subscriptions, sponsorships, or affiliate content.
- Prefer inbound and opt-in acquisition over cold outreach.

## 2. Authorized inbox RAG pattern

Use Google or Gmail data only in the owner's own account and only for approved business workflows.

Recommended flow:

1. Authenticate with minimum required scope.
2. Pull only messages or metadata relevant to the task.
3. Normalize into summaries, tags, and embeddings.
4. Store derived knowledge rather than broad raw exports.
5. Apply retention and deletion rules.

Good uses:

- Customer support search
- Sales pipeline triage
- Supplier and partner intelligence
- Internal operating memory

Rejected uses:

- Extracting contact lists for resale
- Building mass cold-email datasets
- Mining third-party personal contacts without consent

## 3. Phase 1 monetization plan

### Lane A: Productized service

- Offer setup or operations automations to a narrow niche.
- Use the framework to produce repeatable deliverables and SOPs.

### Lane B: Opt-in audience

- Build a newsletter, directory, or private channel.
- Monetize through sponsorships, affiliates, or premium access.

### Lane C: Software workflow

- Package a painkiller tool that saves time for a defined buyer.
- Use inbox RAG only for the owner's internal workflow intelligence.

## 4. Intake gate

Every idea should be checked against:

- legality
- consent
- data provenance
- platform risk
- automation risk

Use `instruments/strategy/score.sh` and the `revenue_planning` tool before committing work.
