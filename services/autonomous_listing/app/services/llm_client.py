from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx
from openai import AsyncOpenAI

from ..config import get_settings


class LLMClient:
    """
    Simple wrapper around OpenAI's chat completions.
    Can be extended to support multiple providers or local models.
    """

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            self._client = None
        else:
            self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model

    async def generate_marketing_copy(
        self,
        prompt: str,
        references: List[str] | None = None,
    ) -> str:
        if not self._client:
            # fallback stub for offline/dev environments
            refs = "\n".join(references or [])
            return f"{prompt}\n\n{refs}".strip()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an empathetic listing copywriter. Generate vivid, concise, "
                    "and persuasive descriptions suitable for marketplaces."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        if references:
            messages.append(
                {
                    "role": "user",
                    "content": "Reference notes:\n" + "\n".join(references),
                }
            )

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.6,
        )
        return response.choices[0].message.content or ""

    async def critique_and_score(
        self,
        draft: str,
        checklist: list[str],
        context: str = "",
    ) -> dict:
        """
        Returns a lightweight JSON-ish critique payload.
        Falls back to deterministic heuristics when no LLM is configured.
        """
        if not self._client:
            score = 0
            notes: list[str] = []
            length = len(draft.strip())
            if length >= 700:
                score += 25
            elif length >= 350:
                score += 15
            else:
                score += 5
                notes.append("Draft is quite short; add specifics, sections, and trust signals.")

            lower = draft.lower()
            hits = 0
            for item in checklist:
                # crude heuristic: look for a keyword from each checklist line
                token = item.split()[0].lower()
                if token and token in lower:
                    hits += 1
            score += min(50, hits * 5)
            if "condition" not in lower:
                notes.append("Add condition details explicitly.")
            if "pickup" not in lower and "ship" not in lower and "delivery" not in lower:
                notes.append("Clarify pickup/shipping/delivery details.")
            score = min(100, score)
            return {"score": score, "strengths": [], "risks": [], "rewrite_notes": notes}

        system = (
            "You are a strict listing copy critic and conversion optimizer.\n"
            "Score the draft on a 0-100 scale and return ONLY valid JSON with keys:\n"
            "score (number), strengths (string[]), risks (string[]), rewrite_notes (string[]).\n"
            "Be concrete, enforce truthfulness, avoid unsupported claims."
        )
        user = (
            f"Context:\n{context}\n\n"
            f"Checklist:\n- " + "\n- ".join(checklist) + "\n\n"
            f"Draft:\n{draft}\n"
        )
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
        )
        content = response.choices[0].message.content or "{}"
        # Best-effort parse; if it fails, return the raw text in notes.
        try:
            import json

            data = json.loads(content)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {"score": 0, "strengths": [], "risks": [], "rewrite_notes": [content]}

    async def extract_attributes_from_images(
        self,
        *,
        notes: str,
        image_urls: List[str],
        schema_hint: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Vision-based attribute extraction.

        If no LLM is configured, returns a minimal heuristic payload.
        """
        if not self._client:
            lower = (notes or "").lower()
            brand = "Hot Wheels" if "hot wheels" in lower else None
            return {
                "brand": brand,
                "product_name": None,
                "series": None,
                "scale": "1:64" if "1:64" in lower else None,
                "condition": None,
                "packaging": "carded" if "card" in lower or "blister" in lower else None,
                "confidence": 0.3,
                "notes": ["LLM not configured; heuristic extraction used."],
            }

        # Prefer a model that supports image inputs; caller controls ALS_OPENAI_MODEL.
        system = (
            "You extract factual product attributes from photos.\n"
            "Return ONLY valid JSON with keys:\n"
            "brand, product_name, series, scale, year, condition, packaging, features (string[]),\n"
            "and per_field_confidence (object mapping field->0..1).\n"
            "Rules:\n"
            "- Do NOT guess. Use null for unknown.\n"
            "- Be conservative; prefer fewer claims with higher confidence.\n"
        )
        if schema_hint:
            system += "\nSchema hint:\n" + str(schema_hint)

        content: List[Dict[str, Any]] = [{"type": "text", "text": f"Seller notes:\n{notes}"}]
        for url in image_urls[:8]:
            content.append({"type": "image_url", "image_url": {"url": url}})

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": content}],
            temperature=0.1,
        )
        raw = response.choices[0].message.content or "{}"
        try:
            import json

            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return {"raw": raw, "notes": ["Failed to parse JSON from vision extraction."]}
