from __future__ import annotations

import re
from typing import Any

from ..llm_client import LLMClient


class DropshipOrchestrator:
    """
    Lightweight orchestrator for one-shot listing generation from scraped product data.

    This implementation intentionally avoids hard dependencies on external workers
    so it can run in constrained environments while preserving extension points.
    """

    def __init__(self) -> None:
        self._llm = LLMClient()

    async def generate_single_listing(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        source_url = str(raw_data.get("source_url") or "")
        title_seed = str(raw_data.get("title") or "High-demand product").strip()
        notes = str(raw_data.get("description") or "").strip()
        supplier_data = raw_data.get("supplier_data") or {}
        images = raw_data.get("images") or []

        supplier_price = self._extract_supplier_price(raw_data)
        price_suggestion = self._price_suggestion(supplier_price)
        tags = self._build_tags(title_seed, notes)

        prompt = (
            "Create an optimized marketplace listing.\n"
            "Return plain text with:\n"
            "1) A concise, high-converting title\n"
            "2) A persuasive description with bullets\n"
            "3) Variant angle ideas for 2 platforms\n\n"
            f"Product title: {title_seed}\n"
            f"Notes: {notes}\n"
            f"Source URL: {source_url}\n"
            f"Suggested sale price: {price_suggestion}\n"
            "Constraints: truthful claims only; no unverifiable specs."
        )
        llm_text = await self._llm.generate_marketing_copy(prompt)

        generated_title = title_seed
        generated_description = llm_text.strip() if llm_text else notes or title_seed

        variants = [
            {
                "platform": "craigslist",
                "angle": "Local pickup urgency and condition clarity",
                "price": price_suggestion,
            },
            {
                "platform": "mercari",
                "angle": "Shipping-ready ecommerce framing",
                "price": price_suggestion,
            },
        ]

        return {
            "title": generated_title,
            "description": generated_description,
            "variants": variants,
            "price_suggestion": price_suggestion,
            "tags": tags,
            "confidence_score": 0.82,
            "source_url": source_url,
            "supplier_data": supplier_data,
            "images": images,
        }

    def _extract_supplier_price(self, raw_data: dict[str, Any]) -> float | None:
        direct = raw_data.get("supplier_price")
        if isinstance(direct, (int, float)) and float(direct) > 0:
            return float(direct)
        text = f"{raw_data.get('title', '')} {raw_data.get('description', '')}"
        match = re.search(r"\$([0-9]+(?:\.[0-9]{1,2})?)", text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def _price_suggestion(self, supplier_price: float | None) -> float:
        if supplier_price and supplier_price > 0:
            return round(max(supplier_price * 1.65, supplier_price + 7.5), 2)
        return 39.99

    def _build_tags(self, title: str, notes: str) -> list[str]:
        corpus = f"{title} {notes}".lower()
        words = re.findall(r"[a-z0-9]{3,}", corpus)
        stop = {
            "with",
            "from",
            "this",
            "that",
            "your",
            "best",
            "high",
            "very",
            "good",
            "great",
            "product",
        }
        tags: list[str] = []
        seen = set()
        for w in words:
            if w in stop or w in seen:
                continue
            seen.add(w)
            tags.append(w)
            if len(tags) >= 8:
                break
        return tags

