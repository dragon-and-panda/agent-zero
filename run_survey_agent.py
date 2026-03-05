import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_bool(value: str | bool | None, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Agent Zero survey_agent directly from a plain Python terminal."
        )
    )
    parser.add_argument(
        "--action",
        default="status",
        choices=[
            "run",
            "run_next",
            "enqueue",
            "discover_urls",
            "create_persona",
            "optimize_profile",
            "status",
        ],
        help="survey_agent action to execute",
    )
    parser.add_argument(
        "--survey-url",
        default="",
        help="direct survey URL (used by run/enqueue)",
    )
    parser.add_argument(
        "--objective",
        default="",
        help="objective text for survey completion",
    )
    parser.add_argument(
        "--user-id",
        default="default",
        help="local user id for profile/persona/session tracking",
    )
    parser.add_argument(
        "--persona",
        default="",
        help="persona text to build/refine and adopt",
    )
    parser.add_argument(
        "--persona-id",
        default="",
        help="use an existing stored persona id",
    )
    parser.add_argument(
        "--adopt-persona",
        default="true",
        help="true/false. If false, skips persona refinement during run",
    )
    parser.add_argument(
        "--source",
        default="manual",
        help="source tag for queued or executed survey",
    )
    parser.add_argument(
        "--mcp-url",
        action="append",
        default=[],
        help="MCP-provided candidate URL. Repeat for multiple values.",
    )
    parser.add_argument(
        "--rag-query",
        default="",
        help="RAG query used to discover candidate survey URLs",
    )
    parser.add_argument(
        "--rag-limit",
        type=int,
        default=5,
        help="max URLs to retrieve from RAG discovery",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=45,
        help="step budget for browser survey completion",
    )
    parser.add_argument(
        "--background-optimize",
        default="true",
        help="true/false. Run profile optimization in background when run completes",
    )
    parser.add_argument(
        "--run-next-count",
        type=int,
        default=1,
        help="when action=run_next, process this many queued surveys sequentially",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print a JSON wrapper with status and raw tool output text",
    )
    parser.add_argument(
        "--auto-install",
        default="true",
        help=(
            "true/false. Automatically run "
            "'python -m pip install -r requirements.txt' if dependencies are missing."
        ),
    )
    return parser


def ensure_dependencies(auto_install: bool):
    try:
        import agent  # noqa: F401
        import initialize  # noqa: F401
        import python.tools.survey_agent  # noqa: F401
        return
    except ModuleNotFoundError as exc:
        if not auto_install:
            raise exc

    requirements = Path(__file__).resolve().parent / "requirements.txt"
    if not requirements.exists():
        raise FileNotFoundError(f"Missing requirements file: {requirements}")

    print("Missing dependencies detected. Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements)])


def create_tool(context, args: dict[str, Any], survey_tool_cls):
    return survey_tool_cls(
        agent=context.agent0,
        name="survey_agent",
        args=args,
        message="run_survey_agent.py direct invocation",
    )


async def invoke_once(context, survey_tool_cls, tool_args: dict[str, Any], as_json: bool):
    tool = create_tool(context, tool_args, survey_tool_cls)
    response = await tool.execute(**tool_args)

    if as_json:
        payload = {
            "ok": True,
            "break_loop": response.break_loop,
            "message": response.message,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(response.message)


async def run():
    parser = build_parser()
    args = parser.parse_args()

    ensure_dependencies(auto_install=parse_bool(args.auto_install, default=True))

    from agent import AgentContext
    from initialize import initialize
    from python.helpers.dotenv import load_dotenv
    from python.tools.survey_agent import SurveyAgent

    load_dotenv()
    config = initialize()
    context = AgentContext(config)

    tool_args = {
        "action": args.action,
        "survey_url": args.survey_url,
        "objective": args.objective,
        "user_id": args.user_id,
        "persona": args.persona,
        "persona_id": args.persona_id,
        "adopt_persona": parse_bool(args.adopt_persona, default=True),
        "source": args.source,
        "mcp_urls": args.mcp_url or [],
        "rag_query": args.rag_query,
        "rag_limit": args.rag_limit,
        "max_steps": args.max_steps,
        "background_optimize": parse_bool(args.background_optimize, default=True),
    }

    if args.action != "run_next":
        await invoke_once(context, SurveyAgent, tool_args, as_json=args.json)
        return

    loops = max(1, int(args.run_next_count))
    for i in range(loops):
        await invoke_once(context, SurveyAgent, tool_args, as_json=args.json)
        # stop early if queue is exhausted
        status_args = {
            "action": "status",
            "user_id": args.user_id,
        }
        status_tool = create_tool(context, status_args, SurveyAgent)
        status_response = await status_tool.execute(**status_args)
        if "pending': 0" in status_response.message or '"pending": 0' in status_response.message:
            if not args.json:
                print(f"Queue appears empty after {i + 1} run_next iterations.")
            break


def main():
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except ModuleNotFoundError as exc:
        print(
            "Dependency error. Re-run with '--auto-install true' or install dependencies manually:\n"
            "python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        print(f"Missing module: {exc}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(
            "Automatic dependency installation failed. Install manually and retry:\n"
            "python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        print(f"Installer exit code: {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode if exc.returncode else 1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
