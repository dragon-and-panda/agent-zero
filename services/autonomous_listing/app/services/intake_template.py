from __future__ import annotations

from typing import Any, Dict, List

from .. import schemas


def _coerce_platforms(platforms: List[str] | None) -> List[schemas.PlatformEnum]:
    if not platforms:
        return [schemas.PlatformEnum.craigslist]
    out: List[schemas.PlatformEnum] = []
    for p in platforms:
        try:
            out.append(schemas.PlatformEnum(p))
        except Exception:
            out.append(schemas.PlatformEnum.custom)
    # de-dup preserve order
    dedup: List[schemas.PlatformEnum] = []
    seen = set()
    for p in out:
        if p.value not in seen:
            seen.add(p.value)
            dedup.append(p)
    return dedup


def platform_checklist(platform: schemas.PlatformEnum) -> List[str]:
    common = [
        "At least 3 clear photos (front/back/close-up); add packaging photos if relevant.",
        "Accurate condition (be explicit about defects).",
        "Clear pickup/shipping plan + location.",
        "Price set (or range/negotiable rules).",
        "No unsupported claims; avoid prohibited items/policies.",
    ]
    per = {
        schemas.PlatformEnum.craigslist: [
            "Pick correct city/area and category.",
            "Keep title concise (≈ 70 chars).",
            "Be explicit about meetup location and payment method.",
        ],
        schemas.PlatformEnum.mercari: [
            "Condition grade + what’s included.",
            "Shipping vs local pickup settings (if applicable).",
        ],
        schemas.PlatformEnum.offerup: [
            "Mobile-first short title; highlight top 3 selling points immediately.",
            "Set meetup safety notes.",
        ],
        schemas.PlatformEnum.nextdoor: [
            "Neighborly tone; include pickup window and cross-street if safe.",
        ],
        schemas.PlatformEnum.etsy: [
            "Materials/tags; ensure category fits Etsy rules.",
            "Processing time + shipping profile (if selling there).",
        ],
        schemas.PlatformEnum.poshmark: [
            "Brand/condition/size details (for apparel).",
            "Bundle-friendly note if relevant.",
        ],
        schemas.PlatformEnum.shopify: [
            "Decide shipping rates/returns policy.",
            "Use a canonical product page structure (Overview/Details/Shipping/Returns/FAQ).",
        ],
    }
    return common + per.get(platform, [])


def listing_intake_template(
    *,
    platforms: List[str] | None = None,
    listing_type: str = "item",
) -> Dict[str, Any]:
    """
    Returns a fill-in template for ListingRequest plus a platform-specific mock preview.
    """
    plats = _coerce_platforms(platforms)
    primary = plats[0]

    # Fill-in template (JSON object users can paste back into create_listing_draft/create_listing)
    template: Dict[str, Any] = {
        "listing_type": listing_type,  # item | event | service
        "title_hint": "",
        "raw_description": "",
        "brand": "",
        "condition": "",
        "dimensions": "",
        "delivery": "",  # local pickup | shipping | delivery | digital
        "event_datetime": "",
        "event_duration": "",
        "category": "",
        "location": "",
        "assets": [
            {
                "source_uri": "https://.../photo1.jpg",
                "caption": "Front/hero shot",
            },
            {
                "source_uri": "https://.../photo2.jpg",
                "caption": "Back/packaging/label shot",
            },
            {
                "source_uri": "https://.../photo3.jpg",
                "caption": "Close-up of condition/defects/serial text",
            },
        ],
        "target_platforms": [p.value for p in plats],
        "preferences": {
            "tone": "premium",
            "min_price": None,
            "target_price": None,
            "pickup_only": False,
        },
    }

    # Platform mock preview (what we’ll generate after you fill the template)
    mock = _mock_listing(primary)
    return {
        "primary_platform": primary.value,
        "target_platforms": [p.value for p in plats],
        "template": template,
        "required_minimum": [
            "raw_description",
            "location (for local platforms)",
            "at least 3 assets (photos)",
        ],
        "platform_checklist": {primary.value: platform_checklist(primary)},
        "mock_listing_preview": mock,
        "how_to_use": [
            "1) Fill in the template fields (leave unknowns blank).",
            "2) Replace asset URLs with your photo URLs (or base64 in `base64_payload`).",
            "3) Send the filled JSON to `create_listing_draft` (safe) or `create_listing` (includes publishing packages).",
        ],
    }


def _mock_listing(platform: schemas.PlatformEnum) -> Dict[str, Any]:
    """
    Example mock listing (Hot Wheels flavored) so users see what “good” looks like.
    """
    if platform == schemas.PlatformEnum.craigslist:
        return {
            "title": "Hot Wheels Cars Lot (Carded + Loose) — Great for Collectors",
            "price": 25,
            "body": (
                "Hot Wheels lot in great condition. Mix of carded and loose cars.\n\n"
                "Highlights:\n"
                "- Assorted models/series (see photos)\n"
                "- Clean, display-ready\n"
                "- Great starter lot for a collection\n\n"
                "Pickup in [Your Area]. Cash/Venmo ok. Message with a time that works."
            ),
            "images_needed": ["hero/front", "packaging backs", "close-ups/rarities/defects"],
        }

    # Generic fallback
    return {
        "title": "Example Title (Brand + Item + Condition + Key Feature)",
        "price": 0,
        "body": "Example description with bullets, condition, logistics, and a clear CTA.",
        "images_needed": ["hero", "details", "condition proof"],
    }

