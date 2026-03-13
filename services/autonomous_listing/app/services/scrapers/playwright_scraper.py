from __future__ import annotations

import re
from urllib.parse import urlparse

import httpx


def _fallback_title_from_url(url: str) -> str:
    parsed = urlparse(url)
    slug = (parsed.path or "").strip("/").split("/")[-1]
    if not slug:
        return parsed.netloc or "Product"
    words = re.split(r"[-_]+", slug)
    return " ".join(w.capitalize() for w in words if w) or "Product"


async def scrape_product_page(url: str) -> dict:
    """
    Lightweight async scraper compatible with environments where Playwright
    is unavailable. It extracts basic metadata and image hints from HTML.
    """
    title = _fallback_title_from_url(url)
    description = ""
    images: list[str] = []

    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text or ""

        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
        if title_match:
            parsed_title = re.sub(r"\s+", " ", title_match.group(1)).strip()
            if parsed_title:
                title = parsed_title

        desc_match = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            html,
            flags=re.I | re.S,
        )
        if desc_match:
            description = re.sub(r"\s+", " ", desc_match.group(1)).strip()

        image_matches = re.findall(
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
            html,
            flags=re.I | re.S,
        )
        images = [img.strip() for img in image_matches if img.strip()][:8]
    except Exception:
        # Fallback keeps endpoint functional even if remote fetch fails.
        pass

    return {
        "source_url": url,
        "title": title,
        "description": description,
        "images": images,
        "supplier_data": {"scrape_mode": "httpx_metadata", "fetched_at": None},
    }

