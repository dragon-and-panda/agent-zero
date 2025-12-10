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
