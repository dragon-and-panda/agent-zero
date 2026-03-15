from __future__ import annotations

import re
from pathlib import Path


DEFAULT_CORPUS = [
    (
        "documentation_phases",
        "For each deliverable, define evidence capture in three phases: before work, during execution, and after completion. "
        "Each phase should include timestamped photos or records plus concise narrative notes.",
    ),
    (
        "acceptance_criteria",
        "Acceptance criteria should be objective, measurable, and tied to explicit standards. "
        "If local authority codes apply, reference the exact code section or permit requirement.",
    ),
    (
        "escrow_controls",
        "Escrow release should follow verified completion evidence and contractual acceptance. "
        "If discrepancies exist, issue remediation addendum and optionally release only undisputed partial amounts.",
    ),
    (
        "arbitration_policy",
        "In disputes, both parties agree to binding platform arbitration based on contract terms, evidence, and audit trail.",
    ),
]


class RAGService:
    def __init__(self, extra_corpus_paths: list[str] | None = None) -> None:
        self._chunks: list[tuple[str, str]] = list(DEFAULT_CORPUS)
        for path in extra_corpus_paths or []:
            self._ingest_file(path)

    def _ingest_file(self, path: str) -> None:
        p = Path(path)
        if not p.exists() or not p.is_file():
            return
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            return
        # Keep chunks small and deterministic for this MVP.
        for idx, para in enumerate(content.split("\n\n")):
            text = para.strip()
            if len(text) < 40:
                continue
            self._chunks.append((f"{p.name}#{idx+1}", text))

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        query_tokens = set(_tokenize(query))
        if not query_tokens:
            return [snippet for _, snippet in self._chunks[:top_k]]
        scored: list[tuple[float, str]] = []
        for source, chunk in self._chunks:
            chunk_tokens = set(_tokenize(chunk))
            overlap = len(query_tokens & chunk_tokens)
            if overlap == 0:
                continue
            score = overlap / max(len(query_tokens), 1)
            scored.append((score, f"{source}: {chunk}"))
        scored.sort(key=lambda x: x[0], reverse=True)
        if not scored:
            return [snippet for _, snippet in self._chunks[:top_k]]
        return [text for _, text in scored[:top_k]]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())
