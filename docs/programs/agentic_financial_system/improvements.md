# Agentic Financial System Improvement Backlog

## Ranked Backlog

### 1. Build a compliant inbox-to-CRM workflow
- **Why:** Fastest path to customer value using first-party business data.
- **Definition of done:** Structured extraction of inbound lead and support events from approved inbox sources with audit metadata.

### 2. Add a revenue lane selector to the orchestration layer
- **Why:** Lets the framework rank opportunities before spinning up sub-agents.
- **Definition of done:** Scoring output becomes an input to mission planning and behavior rules.

### 3. Extend the autonomous listing service with seller analytics
- **Why:** Existing scaffold can be monetized as a managed service faster than building a new product from scratch.
- **Definition of done:** Listing pipeline exposes channel performance, pricing outcomes, and follow-up actions.

### 4. Create prompt personas for compliance and growth
- **Why:** Keeps commercialization agents aligned with policy.
- **Definition of done:** Persona prompts for Venture Analyst, Compliance Guardian, and CRM Operator exist under a dedicated prompt set.

### 5. Add telemetry for legal/consent decisions
- **Why:** The system should prove why it accepted or rejected a workflow.
- **Definition of done:** Every scored lane logs legality, consent, and source-of-truth notes.

### 6. Build a packaged offer library
- **Why:** Reusable offers increase conversion and reduce proposal friction.
- **Definition of done:** Repo contains standardized scopes, deliverables, pricing heuristics, and qualification criteria.

### 7. Add deletion and retention hooks for transient customer data
- **Why:** Lowers privacy risk and makes audits easier.
- **Definition of done:** Temporary working data has a documented retention policy and cleanup path.
