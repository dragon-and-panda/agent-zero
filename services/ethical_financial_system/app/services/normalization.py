import re
from typing import Iterable, List

EMAIL_PATTERN = re.compile(r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$")
ANGLE_BRACKET_PATTERN = re.compile(r"<([^<>]+)>")
CSV_SPLIT_PATTERN = re.compile(r"[;,]")


def normalize_email(raw: str | None) -> str | None:
    if raw is None:
        return None

    candidate = raw.strip().lower()
    if not candidate:
        return None

    if candidate.startswith("mailto:"):
        candidate = candidate[7:].strip()

    bracket_match = ANGLE_BRACKET_PATTERN.search(candidate)
    if bracket_match:
        candidate = bracket_match.group(1).strip()

    candidate = candidate.strip().strip('"').strip("'").strip()

    if not EMAIL_PATTERN.match(candidate):
        return None
    return candidate


def split_contact_cell(cell: str | None) -> List[str]:
    if cell is None:
        return []
    parts = CSV_SPLIT_PATTERN.split(cell)
    return [p.strip() for p in parts if p and p.strip()]


def normalize_many(values: Iterable[str]) -> tuple[List[str], int]:
    deduped: List[str] = []
    seen: set[str] = set()
    invalid_count = 0

    for value in values:
        normalized = normalize_email(value)
        if not normalized:
            invalid_count += 1
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)

    return deduped, invalid_count
