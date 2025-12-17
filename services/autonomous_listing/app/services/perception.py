from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from duckduckgo_search import DDGS

from .. import schemas
from .llm_client import LLMClient


@dataclass
class EvidenceItem:
    source: str
    payload: dict


class PerceptionEngine:
    """
    Minimal, redundancy-first perception pipeline.

    - Extract candidate attributes from images/notes (vision LLM when configured)
    - Scrape web search snippets (DuckDuckGo) as a second independent signal
    - Merge with deterministic consensus scoring
    """

    def __init__(self, llm: LLMClient | None = None) -> None:
        self._llm = llm or LLMClient()

    async def infer_verified_attributes(
        self,
        *,
        request: schemas.ListingRequest,
    ) -> Tuple[Dict[str, str], dict]:
        # Collect image URLs if present (base64 not handled in this MVP).
        image_urls = [str(a.source_uri) for a in request.assets if a.source_uri]
        notes = " ".join(
            x for x in [request.title_hint or "", request.raw_description or ""] if x
        ).strip()

        evidence: List[EvidenceItem] = []

        # Source A: vision extraction (optional)
        vision = await self._llm.extract_attributes_from_images(
            notes=notes,
            image_urls=image_urls,
            schema_hint={
                "use_case": "marketplace_listing",
                "fields": [
                    "brand",
                    "product_name",
                    "series",
                    "scale",
                    "year",
                    "condition",
                    "packaging",
                ],
            },
        )
        evidence.append(EvidenceItem(source="vision_llm", payload=vision if isinstance(vision, dict) else {"raw": vision}))

        # Source B: web search snippets (scrape)
        queries = self._build_queries(request=request, vision=vision)
        web_hits = self._web_search(queries)
        evidence.append(EvidenceItem(source="web_search", payload={"queries": queries, "hits": web_hits}))

        # Source C: user notes as weak evidence
        evidence.append(
            EvidenceItem(
                source="user_notes",
                payload={"notes": notes, "brand": request.brand, "condition": request.condition},
            )
        )

        verified, consensus = self._consensus(evidence)
        report = {"evidence": [e.__dict__ for e in evidence], "consensus": consensus}
        return verified, report

    def _build_queries(self, *, request: schemas.ListingRequest, vision: dict) -> List[str]:
        base_terms: List[str] = []
        for t in [
            request.brand,
            request.title_hint,
            request.category,
        ]:
            if t:
                base_terms.append(t)

        if isinstance(vision, dict):
            for k in ["brand", "product_name", "series", "scale", "year"]:
                v = vision.get(k)
                if isinstance(v, str) and v.strip():
                    base_terms.append(v.strip())

        # Normalize and compress
        joined = " ".join(base_terms).strip()
        joined = re.sub(r"\s+", " ", joined)
        joined = joined[:160]

        # A few redundant variations
        queries = []
        if joined:
            queries.append(joined)
        if request.raw_description:
            snippet = re.sub(r"\s+", " ", request.raw_description)[:120]
            queries.append(snippet)
        # Hot Wheels specific booster if applicable
        if "hot wheels" in (joined.lower() + " " + (request.raw_description or "").lower()):
            queries.append(f"Hot Wheels {joined}".strip())
        # de-dup
        out: List[str] = []
        seen = set()
        for q in queries:
            q = q.strip()
            if not q:
                continue
            k = q.lower()
            if k not in seen:
                seen.add(k)
                out.append(q)
        return out[:4]

    def _web_search(self, queries: List[str]) -> List[dict]:
        hits: List[dict] = []
        try:
            with DDGS() as ddgs:
                for q in queries:
                    for r in ddgs.text(q, max_results=5):
                        hits.append(
                            {
                                "query": q,
                                "title": r.get("title"),
                                "href": r.get("href"),
                                "body": r.get("body"),
                            }
                        )
        except Exception as e:
            hits.append({"error": str(e), "note": "web search failed"})
        return hits[:25]

    def _consensus(self, evidence: List[EvidenceItem]) -> Tuple[Dict[str, str], dict]:
        # Fields we try to verify.
        fields = ["brand", "product_name", "series", "scale", "year", "condition", "packaging"]

        weights = {
            "vision_llm": 0.60,
            "web_search": 0.30,
            "user_notes": 0.20,
        }

        # Collect candidate values with scores.
        candidates: Dict[str, Dict[str, float]] = {f: {} for f in fields}
        provenance: Dict[str, Dict[str, List[str]]] = {f: {} for f in fields}

        def add(field: str, value: str, source: str, conf: float, why: str) -> None:
            v = self._norm(value)
            if not v:
                return
            candidates[field][v] = candidates[field].get(v, 0.0) + weights.get(source, 0.1) * conf
            provenance[field].setdefault(v, []).append(f"{source}: {why}")

        for ev in evidence:
            if ev.source == "vision_llm":
                payload = ev.payload if isinstance(ev.payload, dict) else {}
                per = payload.get("per_field_confidence") if isinstance(payload.get("per_field_confidence"), dict) else {}
                for f in fields:
                    val = payload.get(f)
                    if isinstance(val, str) and val.strip():
                        conf = float(per.get(f, payload.get("confidence", 0.5)) or 0.5)
                        add(f, val, ev.source, max(0.05, min(1.0, conf)), "vision extraction")

            if ev.source == "user_notes":
                payload = ev.payload if isinstance(ev.payload, dict) else {}
                for f in ["brand", "condition"]:
                    val = payload.get(f)
                    if isinstance(val, str) and val.strip():
                        add(f, val, ev.source, 0.6, "provided explicitly")
                notes = payload.get("notes", "")
                if isinstance(notes, str) and notes:
                    # lightweight Hot Wheels signal
                    if "hot wheels" in notes.lower():
                        add("brand", "Hot Wheels", ev.source, 0.5, "notes mention hot wheels")

            if ev.source == "web_search":
                payload = ev.payload if isinstance(ev.payload, dict) else {}
                hits = payload.get("hits", [])
                if isinstance(hits, list):
                    textblob = " ".join(
                        " ".join([h.get("title") or "", h.get("body") or ""])
                        for h in hits
                        if isinstance(h, dict)
                    )
                    lower = textblob.lower()
                    if "hot wheels" in lower:
                        add("brand", "Hot Wheels", ev.source, 0.5, "appears in search snippets")
                    # naive scale extraction
                    if "1:64" in lower or "1/64" in lower:
                        add("scale", "1:64", ev.source, 0.4, "appears in search snippets")

        verified: Dict[str, str] = {}
        uncertainties: Dict[str, dict] = {}
        for f in fields:
            scored = sorted(candidates[f].items(), key=lambda kv: kv[1], reverse=True)
            if not scored:
                continue
            top_v, top_s = scored[0]
            second_s = scored[1][1] if len(scored) > 1 else 0.0
            # Accept if sufficiently strong and not ambiguous.
            if top_s >= 0.45 and (second_s == 0.0 or top_s >= 1.25 * second_s):
                verified[f] = top_v
            else:
                uncertainties[f] = {
                    "top_candidates": scored[:3],
                    "provenance": {k: provenance[f].get(k, []) for k, _ in scored[:3]},
                }

        consensus = {
            "scores": candidates,
            "provenance": provenance,
            "uncertainties": uncertainties,
        }
        return verified, consensus

    def _norm(self, s: str) -> str:
        s = (s or "").strip()
        s = re.sub(r"\s+", " ", s)
        return s

