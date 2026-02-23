### survey_agent:

online survey automation with optional persona adoption and profile optimization
works with browser in python runtime and local survey database
supports url control by direct url, mcp url lists, and rag discovery query

actions:
- run: execute a survey now
- run_next: claim next pending survey from local queue and run it
- enqueue: add survey url to local queue
- discover_urls: list candidate urls from mcp_urls and rag_query
- create_persona: create or refine persona in local chatbot db
- optimize_profile: force profile optimization from captured survey responses
- status: show queue/session/persona/profile optimizer status

usage run:
```json
{
  "thoughts": ["I should complete this survey with a persona."],
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "run",
    "survey_url": "https://example.com/survey",
    "objective": "Complete all pages honestly as a young urban professional persona.",
    "persona": "young urban professional",
    "adopt_persona": true,
    "user_id": "default"
  }
}
```

usage run_next:
```json
{
  "thoughts": ["I should process queued surveys one by one."],
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "run_next",
    "user_id": "default"
  }
}
```

usage enqueue with mcp/rag url options:
```json
{
  "thoughts": ["I should queue survey urls discovered from mcp and rag."],
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "enqueue",
    "mcp_urls": ["https://example.com/form-a", "https://example.com/form-b"],
    "rag_query": "recent consumer opinion surveys with form links",
    "source": "mcp-rag"
  }
}
```
