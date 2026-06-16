#!/usr/bin/env python3

import csv
import json
import sys
from pathlib import Path


ALLOWED_CONSENT = {
    "opt_in",
    "double_opt_in",
    "contractual_opt_in",
    "customer_opt_in",
}
TRUE_VALUES = {"1", "true", "yes", "y"}
BLOCKED_PROVENANCE_TOKENS = {
    "scraped",
    "bought",
    "purchased",
    "gmail",
    "inbox",
    "mailbox",
}
REQUIRED_COLUMNS = {"email", "consent_status", "provenance", "allow_marketing"}


def _normalized(value: str) -> str:
    return (value or "").strip().lower()


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: python /workspace/instruments/custom/consent_contact_extract/consent_contact_extract.py <input_csv> <output_csv>"
        )
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"input file not found: {input_path}")
        return 1

    kept_rows: list[dict[str, str]] = []
    rejected = 0

    with input_path.open(newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        if reader.fieldnames is None:
            print("input csv has no header row")
            return 1

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            print(f"missing required columns: {', '.join(sorted(missing))}")
            return 1

        for row in reader:
            consent_status = _normalized(row.get("consent_status", ""))
            provenance = _normalized(row.get("provenance", ""))
            allow_marketing = _normalized(row.get("allow_marketing", ""))

            if consent_status not in ALLOWED_CONSENT:
                rejected += 1
                continue

            if allow_marketing not in TRUE_VALUES:
                rejected += 1
                continue

            if any(token in provenance for token in BLOCKED_PROVENANCE_TOKENS):
                rejected += 1
                continue

            kept_rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(kept_rows)

    print(
        json.dumps(
            {
                "kept": len(kept_rows),
                "rejected": rejected,
                "output_csv": str(output_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
