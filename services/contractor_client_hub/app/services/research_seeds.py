from __future__ import annotations

import time
from urllib.parse import quote_plus

import pandas as pd
from playwright.sync_api import sync_playwright


def scrape_research_seeds(
    search_query: str, city_subdomain: str = "sfbay", limit: int = 10
) -> list[dict]:
    """Collect lightweight public title seeds for market-language research.

    Notes:
    - Keep request volume low and respect target site terms.
    - This function only extracts public listing titles/snippets, not private data.
    """
    limit = max(1, min(limit, 50))
    url = f"https://{city_subdomain}.craigslist.org/search/bbb?query={quote_plus(search_query)}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(0.75)

        cards = page.locator(".cl-search-result").all()
        seeds: list[dict] = []
        for idx, listing in enumerate(cards[:limit], start=1):
            title_node = listing.locator(".posting-title")
            snippet_node = listing.locator(".meta")
            title = title_node.inner_text().strip() if title_node.count() else ""
            snippet = snippet_node.inner_text().strip() if snippet_node.count() else ""
            if not title:
                continue
            seeds.append({"id": idx, "raw_text": title, "snippet": snippet, "source_url": url})

        browser.close()
        return seeds


def scrape_research_seeds_df(
    search_query: str, city_subdomain: str = "sfbay", limit: int = 10
) -> pd.DataFrame:
    """Pandas helper for downstream analysis."""
    return pd.DataFrame(scrape_research_seeds(search_query, city_subdomain, limit))
