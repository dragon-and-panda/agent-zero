from __future__ import annotations

import re
from typing import List

from duckduckgo_search import DDGS

from .. import schemas


class ProductResearcher:
    """
    Minimal multi-source product discovery.

    This is intentionally simple: search, cluster, score, and return action items.
    """

    def research(self, req: schemas.ProductResearchRequest) -> schemas.ProductResearchResponse:
        queries = self._build_queries(req)
        hits = self._search(queries, max_per_query=max(3, min(8, req.max_results)))
        candidates = self._derive_candidates(req, hits)
        candidates = sorted(candidates, key=lambda c: c.score, reverse=True)[: req.max_results]
        return schemas.ProductResearchResponse(niche=req.niche, candidates=candidates, notes=[f"queries={queries}"])

    def _build_queries(self, req: schemas.ProductResearchRequest) -> List[str]:
        base = req.niche.strip()
        loc = f" {req.location}" if req.location else ""
        q = [
            f"best selling {base} 2025",
            f"high demand {base} trending",
            f"{base} price guide",
            f"{base} sold listings",
            f"{base} resale value",
        ]
        if req.location:
            q.append(f"{base} deals{loc} craigslist")
            q.append(f"{base} deals{loc} facebook marketplace")
        # de-dup
        out: List[str] = []
        seen = set()
        for s in q:
            s = re.sub(r"\s+", " ", s).strip()
            k = s.lower()
            if k and k not in seen:
                seen.add(k)
                out.append(s)
        return out[:8]

    def _search(self, queries: List[str], max_per_query: int) -> List[dict]:
        hits: List[dict] = []
        with DDGS() as ddgs:
            for q in queries:
                for r in ddgs.text(q, max_results=max_per_query):
                    hits.append(
                        {
                            "query": q,
                            "title": r.get("title") or "",
                            "href": r.get("href") or "",
                            "body": r.get("body") or "",
                        }
                    )
        return hits

    def _derive_candidates(self, req: schemas.ProductResearchRequest, hits: List[dict]) -> List[schemas.ProductCandidate]:
        # Very small heuristic: extract repeated noun-ish phrases from titles.
        phrases: dict[str, dict] = {}
        stop = set(["the", "and", "for", "with", "best", "top", "2025", "guide", "review", "vs"])
        for h in hits:
            title = h.get("title", "")
            words = [w.lower() for w in re.findall(r"[A-Za-z0-9']{3,}", title)]
            # build 2-3 word shingles
            for n in (2, 3):
                for i in range(0, max(0, len(words) - n + 1)):
                    chunk = words[i : i + n]
                    if any(w in stop for w in chunk):
                        continue
                    phrase = " ".join(chunk)
                    phrases.setdefault(phrase, {"count": 0, "links": set(), "titles": set()})
                    phrases[phrase]["count"] += 1
                    if h.get("href"):
                        phrases[phrase]["links"].add(h["href"])
                    phrases[phrase]["titles"].add(title)

        # Score phrases by redundancy and basic goal fit.
        out: List[schemas.ProductCandidate] = []
        for phrase, meta in phrases.items():
            if meta["count"] < 2:
                continue
            score = min(100.0, 25.0 + meta["count"] * 12.0)
            risks: List[str] = []
            if "replica" in phrase or "fake" in phrase:
                risks.append("Counterfeit risk signal in keywords.")
                score -= 15
            if any("avoid counterfeit" in c.lower() for c in req.constraints):
                # penalize brand-heavy niches generically
                if any(w in phrase for w in ["nike", "adidas", "supreme", "lululemon"]):
                    risks.append("Brand-heavy niche; higher counterfeit risk.")
                    score -= 10

            why = f"Repeated across sources ({meta['count']} mentions)."
            kws = phrase.split()
            links = list(meta["links"])[:5]
            out.append(
                schemas.ProductCandidate(
                    title=phrase.title(),
                    why=why,
                    keywords=kws,
                    evidence_links=links,
                    score=max(0.0, min(100.0, score)),
                    risks=risks,
                    suggested_next_step=(
                        "Validate by checking sold comps (eBay/Etsy) and confirming sourcing cost + shipping."
                    ),
                )
            )
        return out

