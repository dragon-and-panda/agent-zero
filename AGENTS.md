# AGENTS.md

## Cursor Cloud specific instructions

### Overview

Agent Zero is a Python-based AI agent framework with a Flask Web UI. The main entry point is `run_ui.py`. See `docs/installation.md` and `docs/quickstart.md` for detailed setup and usage documentation.

### Running the main application

```bash
source /workspace/venv/bin/activate
python run_ui.py --port 5000 --host 0.0.0.0
```

The Web UI serves on `http://localhost:5000` by default. Port can be overridden via `--port` or the `WEB_UI_PORT` env var.

### Supplementary services

- **Collab Doc** (FastAPI WebSocket relay): `cd /workspace/services/collab_doc && uvicorn app.main:app --port 8002`
- **Autonomous Listing** has a pre-existing circular import bug (`publisher.py` ↔ `orchestrator.py`) and cannot start as of this writing.

### Key caveats

- **Virtual environment**: Dependencies are installed in `/workspace/venv`. Always activate it before running anything: `source /workspace/venv/bin/activate`.
- **`openai-whisper` build**: The `openai-whisper` package requires `--no-build-isolation` during pip install because its `setup.py` uses `pkg_resources` which is missing from newer setuptools build environments. The update script handles this automatically.
- **No formal test suite or linter config**: The repository does not include pytest tests, a `pyproject.toml`, or linter configuration (ruff/flake8/etc.). Linting and testing are not applicable unless added.
- **LLM API keys required for chat**: The Web UI starts without API keys, but sending messages requires at least one LLM provider key (e.g., `API_KEY_OPENAI`). Keys are configured via the Settings page in the UI or in `.env`.
- **Settings persistence**: Settings are stored in `tmp/settings.json`; sensitive values (API keys, passwords) go into `.env`.
- **`flask-socketio`**: Required by `python/collaboration.py` but not listed in `requirements.txt`. The update script installs it separately.
