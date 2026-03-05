import inspect
import json
import uuid
from typing import Any

import models
from pydantic import BaseModel, Field

from python.helpers import dirty_json, files
from python.helpers.browser_use import browser_use
from python.helpers.survey_runtime import (
    discover_urls_with_rag,
    extract_urls,
    get_survey_runtime,
    is_http_url,
)
from python.helpers.tool import Response, Tool


class SurveyAnswer(BaseModel):
    question: str
    answer: str
    rationale: str = ""
    confidence: float = 0.0


class SurveyDoneResult(BaseModel):
    completion_status: str = "completed"
    summary: str = ""
    final_url: str = ""
    title: str = ""
    responses: list[SurveyAnswer] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)


class SurveyAgent(Tool):
    async def execute(
        self,
        action: str = "run",
        survey_url: str = "",
        objective: str = "",
        user_id: str = "default",
        persona: str = "",
        persona_id: str = "",
        adopt_persona: bool = True,
        source: str = "manual",
        mcp_urls: list[str] | str | None = None,
        rag_query: str = "",
        rag_limit: int = 5,
        max_steps: int = 45,
        background_optimize: bool = True,
        **kwargs,
    ):
        runtime = get_survey_runtime(self.agent)
        action_name = (action or "run").strip().lower()
        rag_limit = self._to_int(rag_limit, default=5)
        max_steps = self._to_int(max_steps, default=45)
        mcp_url_list = self._to_url_list(mcp_urls)

        if action_name == "status":
            status = runtime.db.get_status_summary(user_id=user_id)
            return Response(message=self._format_status(status), break_loop=False)

        if action_name == "discover_urls":
            urls = await self._discover_urls(
                mcp_urls=mcp_url_list,
                rag_query=rag_query,
                rag_limit=rag_limit,
            )
            if not urls:
                return Response(
                    message="No candidate survey URLs found from MCP inputs or RAG query.",
                    break_loop=False,
                )
            message = "Discovered survey URLs:\n" + "\n".join(f"- {url}" for url in urls)
            return Response(message=message, break_loop=False)

        if action_name == "enqueue":
            chosen, _, discovered = await self._resolve_url(
                runtime=runtime,
                survey_url=survey_url,
                source=source,
                mcp_urls=mcp_url_list,
                rag_query=rag_query,
                rag_limit=rag_limit,
                allow_queue=False,
            )
            if not chosen:
                return Response(
                    message=(
                        "Unable to enqueue survey because no valid URL was provided. "
                        "Pass survey_url, mcp_urls, or rag_query."
                    ),
                    break_loop=False,
                )
            item = runtime.db.enqueue_survey(
                url=chosen,
                source=source,
                metadata={
                    "objective": objective,
                    "persona": persona,
                    "persona_id": persona_id,
                    "mcp_urls": mcp_url_list,
                    "rag_query": rag_query,
                    "discovered_urls": discovered,
                },
            )
            return Response(
                message=(
                    f"Survey queued.\n"
                    f"- queue_id: {item['id']}\n"
                    f"- url: {item['url']}\n"
                    f"- source: {item['source']}\n"
                    f"- status: {item['status']}"
                ),
                break_loop=False,
            )

        if action_name == "create_persona":
            persona_data = await runtime.chatbot.refine_persona(
                agent=self.agent,
                user_id=user_id,
                objective=objective,
                requested_persona=persona,
                persona_id=persona_id,
                background=False,
            )
            return Response(
                message=(
                    "Persona updated:\n"
                    f"- id: {persona_data['id']}\n"
                    f"- name: {persona_data['name']}\n"
                    f"- description: {persona_data['description']}\n"
                    f"- instructions: {persona_data['instructions']}"
                ),
                break_loop=False,
            )

        if action_name == "optimize_profile":
            result = await runtime.run_optimizer_now(
                agent=self.agent, user_id=user_id, force=True
            )
            if not result:
                return Response(
                    message=(
                        "Profile optimizer skipped because there are not enough "
                        "new survey responses to learn from yet."
                    ),
                    break_loop=False,
                )
            return Response(
                message=(
                    "Profile optimization completed:\n"
                    f"- run_id: {result['run_id']}\n"
                    f"- responses_used: {result['response_count']}\n"
                    f"- summary: {result['summary']}"
                ),
                break_loop=False,
            )

        if action_name not in {"run", "run_next"}:
            return Response(
                message=(
                    f"Unsupported action '{action_name}'. "
                    "Supported actions: run, run_next, enqueue, discover_urls, "
                    "create_persona, optimize_profile, status."
                ),
                break_loop=False,
            )

        chosen_url, queue_item, discovered = await self._resolve_url(
            runtime=runtime,
            survey_url=survey_url,
            source=source,
            mcp_urls=mcp_url_list,
            rag_query=rag_query,
            rag_limit=rag_limit,
            allow_queue=(action_name == "run_next"),
        )
        if not chosen_url:
            return Response(
                message=(
                    "No survey URL available to run. Use survey_url, provide mcp_urls, "
                    "set rag_query, or enqueue surveys and call action='run_next'."
                ),
                break_loop=False,
            )

        if queue_item:
            queue_metadata = queue_item.get("metadata", {})
            if not objective:
                objective = str(queue_metadata.get("objective", ""))
            if not persona:
                persona = str(queue_metadata.get("persona", ""))
            if not persona_id:
                persona_id = str(queue_metadata.get("persona_id", ""))
            source = str(queue_item.get("source") or source)

        persona_data = None
        if self._as_bool(adopt_persona, default=True):
            persona_data = await runtime.chatbot.refine_persona(
                agent=self.agent,
                user_id=user_id,
                objective=objective,
                requested_persona=persona,
                persona_id=persona_id,
                background=False,
            )
        elif persona_id:
            persona_data = runtime.db.get_persona(persona_id)

        profile = runtime.db.get_profile(user_id=user_id)
        session_id = str(uuid.uuid4())
        queue_id = queue_item["id"] if queue_item else None

        runtime.db.create_session(
            session_id=session_id,
            user_id=user_id,
            survey_url=chosen_url,
            source=source,
            objective=objective,
            persona_id=(persona_data or {}).get("id"),
            queue_id=queue_id,
        )

        runtime.mark_survey_active()
        self.agent.context.log.set_progress("Survey: running browser workflow")
        browser_result: dict[str, Any] = {}
        try:
            browser_result = await self._complete_survey_in_browser(
                survey_url=chosen_url,
                objective=objective,
                persona_data=persona_data,
                profile=profile,
                max_steps=max_steps,
            )
            responses = browser_result.get("responses", [])
            runtime.db.add_survey_responses(
                session_id=session_id, user_id=user_id, responses=responses
            )

            final_status = str(browser_result.get("completion_status", "partial"))
            final_summary = str(browser_result.get("summary", "Survey run completed."))
            runtime.db.complete_session(
                session_id=session_id,
                status=final_status,
                summary=final_summary,
                raw_result=browser_result,
            )
            if queue_id:
                queue_status = "completed" if final_status == "completed" else "partial"
                runtime.db.update_queue_status(queue_id=queue_id, status=queue_status)

            if self._as_bool(background_optimize, default=True):
                runtime.maybe_start_background_optimizer(self.agent, user_id=user_id)

            return Response(
                message=self._format_run_result(
                    session_id=session_id,
                    url=chosen_url,
                    source=source,
                    objective=objective,
                    persona_data=persona_data,
                    result=browser_result,
                    discovered_urls=discovered,
                ),
                break_loop=False,
            )
        except Exception as e:
            runtime.db.fail_session(session_id=session_id, error=str(e))
            if queue_id:
                runtime.db.update_queue_status(queue_id=queue_id, status="failed")
            raise e
        finally:
            runtime.mark_survey_inactive()
            self.agent.context.log.set_progress("")

    async def _discover_urls(
        self, mcp_urls: list[str], rag_query: str, rag_limit: int
    ) -> list[str]:
        urls: list[str] = []
        seen = set()
        for url in mcp_urls:
            if is_http_url(url) and url not in seen:
                seen.add(url)
                urls.append(url)

        rag_urls = await discover_urls_with_rag(
            self.agent, rag_query, limit=max(rag_limit, 1)
        )
        for url in rag_urls:
            if is_http_url(url) and url not in seen:
                seen.add(url)
                urls.append(url)
        return urls

    async def _resolve_url(
        self,
        runtime,
        survey_url: str,
        source: str,
        mcp_urls: list[str],
        rag_query: str,
        rag_limit: int,
        allow_queue: bool,
    ) -> tuple[str, dict[str, Any] | None, list[str]]:
        discovered: list[str] = []
        queue_item = None
        chosen_url = ""

        if is_http_url(survey_url):
            chosen_url = survey_url.strip()
        else:
            discovered = await self._discover_urls(
                mcp_urls=mcp_urls,
                rag_query=rag_query,
                rag_limit=rag_limit,
            )
            if discovered:
                chosen_url = discovered[0]

        if not chosen_url and allow_queue:
            queue_item = runtime.db.claim_next_survey()
            if queue_item:
                queue_url = str(queue_item.get("url", ""))
                if is_http_url(queue_url):
                    chosen_url = queue_url

        return chosen_url, queue_item, discovered

    def _to_url_list(self, values: list[str] | str | None) -> list[str]:
        if values is None:
            return []
        if isinstance(values, list):
            merged = "\n".join(str(item) for item in values)
            return [url for url in extract_urls(merged) if is_http_url(url)]
        text = str(values)
        urls = extract_urls(text)
        if urls:
            return [url for url in urls if is_http_url(url)]

        # Allow comma/newline separated plain URLs without punctuation
        out: list[str] = []
        for part in text.replace("\n", ",").split(","):
            url = part.strip()
            if is_http_url(url):
                out.append(url)
        return out

    @staticmethod
    def _as_bool(value: Any, default: bool = False) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return default
        text = str(value).strip().lower()
        if text in {"1", "true", "yes", "y", "on"}:
            return True
        if text in {"0", "false", "no", "n", "off"}:
            return False
        return default

    @staticmethod
    def _to_int(value: Any, default: int) -> int:
        try:
            return int(value)
        except Exception:
            return default

    async def _complete_survey_in_browser(
        self,
        survey_url: str,
        objective: str,
        persona_data: dict[str, Any] | None,
        profile: dict[str, Any],
        max_steps: int,
    ) -> dict[str, Any]:
        browser = None
        context = None

        class SurveySystemPrompt(browser_use.SystemPrompt):
            def important_rules(self) -> str:
                base_rules = super().important_rules()
                survey_rules = """
You are filling online surveys inside a controlled browser session.
Always open the provided survey URL first.
Follow persona/profile instructions consistently when answering.
Never request or invent sensitive account credentials.
If blocked by login, captcha, paywall, or missing permissions, stop and report blockers.
When done, call action "Done with task" with structured fields:
completion_status, summary, final_url, responses, blockers.
"""
                return f"{base_rules}\n{survey_rules}".strip()

        controller = browser_use.Controller()

        @controller.registry.action("Done with task", param_model=SurveyDoneResult)
        async def done(params: SurveyDoneResult):
            result = browser_use.ActionResult(
                is_done=True,
                extracted_content=params.model_dump_json(),
            )
            return result

        model = models.get_model(
            type=models.ModelType.CHAT,
            provider=self.agent.config.browser_model.provider,
            name=self.agent.config.browser_model.name,
            **self.agent.config.browser_model.kwargs,
        )

        task = self._build_browser_task(
            survey_url=survey_url,
            objective=objective,
            persona_data=persona_data,
            profile=profile,
            max_steps=max_steps,
        )

        try:
            browser = browser_use.Browser(
                config=browser_use.BrowserConfig(
                    headless=True,
                    disable_security=True,
                )
            )
            context = await browser.new_context()
            await context._initialize_session()
            pw_context = context.session.context  # type: ignore
            js_override = files.get_abs_path("lib/browser/init_override.js")
            await pw_context.add_init_script(path=js_override)  # type: ignore

            survey_agent = browser_use.Agent(
                task=task,
                browser_context=context,
                llm=model,
                use_vision=self.agent.config.browser_model.vision,
                system_prompt_class=SurveySystemPrompt,
                controller=controller,
            )

            run_kwargs = {}
            run_signature = inspect.signature(survey_agent.run)
            if "max_steps" in run_signature.parameters:
                run_kwargs["max_steps"] = max(1, int(max_steps))

            run_result = await survey_agent.run(**run_kwargs)
            raw = run_result.final_result() if run_result else ""
            return self._parse_browser_result(raw)
        finally:
            await self._safe_close(context)
            await self._safe_close(browser)

    def _build_browser_task(
        self,
        survey_url: str,
        objective: str,
        persona_data: dict[str, Any] | None,
        profile: dict[str, Any],
        max_steps: int,
    ) -> str:
        persona_text = "No explicit persona requested. Use profile-consistent neutral answers."
        if persona_data:
            persona_text = json.dumps(
                {
                    "id": persona_data.get("id"),
                    "name": persona_data.get("name"),
                    "description": persona_data.get("description"),
                    "instructions": persona_data.get("instructions"),
                    "traits": persona_data.get("traits", {}),
                },
                indent=2,
            )

        profile_text = json.dumps(profile or {}, indent=2)
        if len(profile_text) > 4000:
            profile_text = profile_text[:4000] + "\n...truncated..."

        objective_text = objective.strip() or "Complete the survey carefully and consistently."

        return (
            f"Open this survey URL first: {survey_url}\n\n"
            f"Primary objective:\n{objective_text}\n\n"
            f"Persona guidance:\n{persona_text}\n\n"
            f"Current user profile data:\n{profile_text}\n\n"
            "Execution requirements:\n"
            f"- Stay within approximately {max(1, int(max_steps))} steps.\n"
            "- Answer all visible questions you can access.\n"
            "- Track each answered question in your working memory.\n"
            "- If blocked, provide blocker details and finish.\n"
            "- End with action 'Done with task' using structured JSON fields:\n"
            "  completion_status, summary, final_url, responses, blockers.\n"
            "- In responses include: question, answer, rationale, confidence(0-1).\n"
        )

    def _parse_browser_result(self, raw: str) -> dict[str, Any]:
        parsed: dict[str, Any] = {}
        if raw:
            try:
                item = json.loads(raw)
                if isinstance(item, dict):
                    parsed = item
            except Exception:
                pass
            if not parsed:
                try:
                    item = dirty_json.DirtyJson.parse_string(raw)
                    if isinstance(item, dict):
                        parsed = item
                except Exception:
                    pass

        if not parsed:
            return {
                "completion_status": "partial",
                "summary": str(raw).strip() or "Survey completed without structured output.",
                "final_url": "",
                "responses": [],
                "blockers": [],
            }

        status = str(
            parsed.get("completion_status")
            or parsed.get("status")
            or "partial"
        ).strip().lower()
        if status not in {"completed", "partial", "blocked", "failed"}:
            status = "partial"

        summary = str(
            parsed.get("summary")
            or parsed.get("response")
            or parsed.get("page_summary")
            or "Survey run completed."
        ).strip()
        final_url = str(parsed.get("final_url") or "").strip()

        responses_raw = parsed.get("responses", [])
        responses: list[dict[str, Any]] = []
        if isinstance(responses_raw, list):
            for item in responses_raw:
                if not isinstance(item, dict):
                    continue
                question = str(item.get("question", "")).strip()
                answer = str(item.get("answer", "")).strip()
                if not question or not answer:
                    continue
                rationale = str(item.get("rationale", "")).strip()
                confidence_raw = item.get("confidence", 0.0)
                try:
                    confidence = float(confidence_raw)
                except Exception:
                    confidence = 0.0
                confidence = max(0.0, min(1.0, confidence))
                responses.append(
                    {
                        "question": question,
                        "answer": answer,
                        "rationale": rationale,
                        "confidence": confidence,
                    }
                )

        blockers_raw = parsed.get("blockers", [])
        blockers: list[str] = []
        if isinstance(blockers_raw, list):
            blockers = [str(item).strip() for item in blockers_raw if str(item).strip()]

        return {
            "completion_status": status,
            "summary": summary,
            "final_url": final_url,
            "responses": responses,
            "blockers": blockers,
        }

    async def _safe_close(self, obj):
        if not obj:
            return
        close_fn = getattr(obj, "close", None)
        if not callable(close_fn):
            return
        try:
            maybe_awaitable = close_fn()
            if inspect.isawaitable(maybe_awaitable):
                await maybe_awaitable
        except Exception:
            pass

    def _format_status(self, status: dict[str, Any]) -> str:
        queue = status.get("queue", {})
        sessions = status.get("sessions", {})
        return (
            "Survey agent status:\n"
            f"- personas: {status.get('persona_count', 0)}\n"
            f"- queue: {queue}\n"
            f"- sessions: {sessions}\n"
            f"- unoptimized_responses: {status.get('unoptimized_responses', 0)}\n"
            f"- db_path: {status.get('db_path', '')}"
        )

    def _format_run_result(
        self,
        session_id: str,
        url: str,
        source: str,
        objective: str,
        persona_data: dict[str, Any] | None,
        result: dict[str, Any],
        discovered_urls: list[str],
    ) -> str:
        persona_id = (persona_data or {}).get("id", "")
        responses = result.get("responses", [])
        blockers = result.get("blockers", [])

        lines = [
            "Survey session completed.",
            f"- session_id: {session_id}",
            f"- status: {result.get('completion_status', 'partial')}",
            f"- url: {url}",
            f"- source: {source}",
            f"- objective: {objective or 'n/a'}",
            f"- persona_id: {persona_id or 'none'}",
            f"- responses_captured: {len(responses)}",
            f"- blockers: {len(blockers)}",
            f"- summary: {result.get('summary', '')}",
        ]

        final_url = str(result.get("final_url", "")).strip()
        if final_url:
            lines.append(f"- final_url: {final_url}")

        if discovered_urls:
            lines.append("- discovered_candidates:")
            lines.extend(f"  - {item}" for item in discovered_urls[:5])

        if blockers:
            lines.append("- blocker_details:")
            lines.extend(f"  - {item}" for item in blockers[:5])

        if responses:
            lines.append("- sample_responses:")
            for response in responses[:3]:
                lines.append(
                    f"  - Q: {response['question']} | A: {response['answer']}"
                )

        return "\n".join(lines)
