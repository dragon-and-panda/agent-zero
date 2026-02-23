# Survey Agent

The Survey Agent adds a persona-aware survey automation workflow to Agent Zero. It is implemented as a tool named `survey_agent` and uses the existing Python browser runtime.

## What it does

- Completes online surveys through a browser session controlled in Python.
- Optionally adopts a persona before answering.
- Captures survey question/answer pairs into a local database.
- Maintains a local persona/profile database.
- Runs a background profile optimizer chatbot while the agent is idle (not actively filling surveys).

## Components

### 1) Tool: `python/tools/survey_agent.py`

Primary orchestration entry point with actions:

- `run` - run one survey now.
- `run_next` - run the next queued survey.
- `enqueue` - add a survey URL to queue.
- `discover_urls` - gather candidate URLs from MCP-supplied URLs and/or RAG query.
- `create_persona` - create or refine persona.
- `optimize_profile` - force profile optimization now.
- `status` - inspect queue/session/profile state.

### 2) Runtime + Local DB: `python/helpers/survey_runtime.py`

Provides:

- SQLite-backed storage for:
  - personas,
  - user profiles,
  - survey queue,
  - survey sessions,
  - survey responses,
  - optimizer run history.
- URL helpers for parsing and RAG URL discovery.
- Local chatbot routines for:
  - persona refinement,
  - profile optimization from survey responses.

Default database path:

`memory/<memory_subdir-or-default>/survey_agent/survey_agent.db`

### 3) Background optimizer extension

`python/extensions/message_loop_end/_40_survey_profile_optimizer.py`

After each message loop:

- if the survey tool runtime exists and is **not busy**,
- schedule a best-effort background optimization pass
- to merge new survey responses into the stored profile.

## URL sourcing strategy

The tool supports multiple URL sources:

1. **Direct URL** via `survey_url`.
2. **MCP-provided URLs** via `mcp_urls` (string or list).
3. **RAG discovery** via `rag_query` using the memory/knowledge vector DB.
4. **Queue** via `enqueue` and `run_next`.

## Persona and profile lifecycle

1. Persona is generated/refined by the local chatbot (`create_persona` or `run` with `adopt_persona=true`).
2. Survey run captures responses (`question`, `answer`, `rationale`, `confidence`).
3. Background optimizer consumes unoptimized responses and updates the user profile.
4. Updated profile is reused in future survey runs.

## Example tool calls

### Add a real survey source (Freecash)

User-provided survey listing:

- `https://freecash.com/surveys`

You can queue it directly:

```json
{
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "enqueue",
    "survey_url": "https://freecash.com/surveys",
    "source": "freecash"
  }
}
```

### Run one survey with persona

```json
{
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "run",
    "survey_url": "https://example.com/survey",
    "objective": "Complete all pages consistently.",
    "persona": "tech-savvy parent in a suburban area",
    "user_id": "default"
  }
}
```

### Queue and process surveys

```json
{
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "enqueue",
    "survey_url": "https://example.com/s1"
  }
}
```

```json
{
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "run_next",
    "user_id": "default"
  }
}
```

### Force profile optimization

```json
{
  "tool_name": "survey_agent",
  "tool_args": {
    "action": "optimize_profile",
    "user_id": "default"
  }
}
```
