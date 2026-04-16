# Agentic Financial System Improvement Backlog

## Priority 1

### Inbox-to-CRM specification
- define entity schema for lead, contact, company, conversation, task, and opportunity;
- define provenance fields for every extracted record;
- decide how much raw email content can be stored versus summarized.

### Mailbox safety controls
- require explicit account authorization;
- define retention and deletion rules;
- document allowed versus prohibited extraction behaviors.

### Opportunity scoring workflow
- keep a simple gate that rejects lanes with low legality, consent, provenance, or TOS alignment;
- record score decisions in the mission diary.

## Priority 2

### CRM integration layer
- identify safe export targets such as CSV, Notion, or a lightweight CRM payload;
- add deduplication rules for repeated senders and aliases.

### Operator dashboard
- show active lanes, decision history, and blocked ideas;
- expose why a lane was rejected or placed on hold.

### Listing-service reuse
- connect this program to the adjacent autonomous listing work as a hedge lane.

## Priority 3

### Research product lane
- define product templates for niche briefings and intelligence reports;
- create a repeatable packaging workflow for paid deliverables.

### Client automation lane
- create standard discovery prompts and intake templates for client-authorized data work;
- define safe deployment boundaries and review checkpoints.
