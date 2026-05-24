import json

from python.helpers.tool import Tool, Response


HARD_GATES = ("legality", "consent", "provenance", "tos")
SOFT_GATES = ("time", "margin", "repeatability", "automation", "defensibility")
VALID_DECISIONS = {"approve", "hold", "reject"}


class RevenuePlanning(Tool):
    async def execute(
        self,
        lane_name: str = "",
        summary: str = "",
        data_sources: str = "",
        hard_gates_json: str = "",
        soft_gates_json: str = "",
        notes: str = "",
        **kwargs,
    ):
        if not lane_name.strip():
            return Response(
                message="lane_name is required.",
                break_loop=False,
            )

        parsed_data_sources = _parse_list(data_sources)
        hard_gates = _parse_gate_dict(hard_gates_json, HARD_GATES)
        soft_gates = _parse_gate_dict(soft_gates_json, SOFT_GATES)

        disallowed_hits = _find_disallowed_patterns(
            " ".join(
                [
                    lane_name,
                    summary,
                    notes,
                    " ".join(parsed_data_sources),
                ]
            )
        )

        hard_failures = [name for name, value in hard_gates.items() if value != "pass"]
        soft_failures = [name for name, value in soft_gates.items() if value != "strong"]

        if disallowed_hits:
            decision = "reject"
            rationale = (
                "The lane depends on prohibited personal-data extraction, list resale, "
                "or unauthorized outreach patterns."
            )
        elif hard_failures:
            decision = "reject"
            rationale = (
                "One or more hard gates failed: " + ", ".join(sorted(hard_failures)) + "."
            )
        elif soft_failures:
            decision = "hold"
            rationale = (
                "Hard gates passed, but these execution factors need improvement: "
                + ", ".join(sorted(soft_failures))
                + "."
            )
        else:
            decision = "approve"
            rationale = "The lane passed all hard gates and the execution profile is attractive."

        safe_alternatives = _safe_alternatives(disallowed_hits)

        result = {
            "lane_name": lane_name,
            "decision": decision,
            "summary": summary,
            "data_sources": parsed_data_sources,
            "hard_gates": hard_gates,
            "soft_gates": soft_gates,
            "hard_failures": sorted(hard_failures),
            "soft_failures": sorted(soft_failures),
            "policy_hits": disallowed_hits,
            "rationale": rationale,
            "safe_alternatives": safe_alternatives,
            "notes": notes,
        }
        return Response(
            message=json.dumps(result, indent=2),
            break_loop=False,
        )


def _parse_list(raw_value: str) -> list[str]:
    if not raw_value.strip():
        return []
    try:
        parsed = json.loads(raw_value)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except Exception:
        pass
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _parse_gate_dict(raw_value: str, expected_keys: tuple[str, ...]) -> dict[str, str]:
    defaults = {key: "unknown" for key in expected_keys}
    if not raw_value.strip():
        return defaults

    try:
        parsed = json.loads(raw_value)
    except Exception as exc:
        defaults["parse_error"] = str(exc)
        return defaults

    if not isinstance(parsed, dict):
        defaults["parse_error"] = "JSON value must be an object."
        return defaults

    result = defaults.copy()
    for key in expected_keys:
        if key in parsed:
            result[key] = str(parsed[key]).strip().lower()
    return result


def _find_disallowed_patterns(text: str) -> list[str]:
    normalized = text.lower()
    patterns = {
        "email_list_sale": ("sell email list", "selling email list", "broker email list"),
        "personal_data_harvesting": ("harvest email", "scrape inbox", "extract gmail"),
        "unauthorized_outreach": ("cold outreach from scraped", "unsolicited bulk email", "spam"),
    }
    hits = []
    for label, keywords in patterns.items():
        if any(keyword in normalized for keyword in keywords):
            hits.append(label)
    return hits


def _safe_alternatives(policy_hits: list[str]) -> list[str]:
    if not policy_hits:
        return []
    return [
        "Inbox-to-CRM workflow for first-party or client-authorized data",
        "Opt-in lead magnet or research product instead of personal-data resale",
        "Client-owned outreach operations using lawfully obtained contacts",
        "Marketplace listing optimization or other service-based monetization",
    ]
