#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_SOURCES = {"first_party", "licensed", "opt_in"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract only consented contacts from owner-authorized data."
    )
    parser.add_argument("--input", required=True, help="Input JSON file path.")
    parser.add_argument("--output", required=True, help="Output JSON file path.")
    parser.add_argument(
        "--owner-authorized",
        action="store_true",
        help="Confirm that the operator owns or is authorized to use the dataset.",
    )
    parser.add_argument(
        "--allowed-domains",
        default="",
        help="Comma-separated allowlist of email domains. Empty means no domain filter.",
    )
    return parser.parse_args()


def normalize_domain_list(value: str) -> set[str]:
    domains = set()
    for item in value.split(","):
        cleaned = item.strip().lower()
        if cleaned:
            domains.add(cleaned)
    return domains


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value or ""))


def truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    if isinstance(value, int):
        return value != 0
    return False


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    allowed_domains = normalize_domain_list(args.allowed_domains)

    records = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Input must be a JSON list of contact records.")

    accepted: list[dict] = []
    rejected: list[dict] = []

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            rejected.append({"index": index, "reason": "record is not an object"})
            continue

        email = str(record.get("email", "")).strip().lower()
        consent = truthy(record.get("consent"))
        source = str(record.get("source", "")).strip().lower()
        record_authorized = args.owner_authorized or truthy(
            record.get("owner_authorized")
        )

        if not record_authorized:
            rejected.append(
                {
                    "index": index,
                    "email": email,
                    "reason": "missing owner authorization",
                }
            )
            continue
        if not is_valid_email(email):
            rejected.append(
                {"index": index, "email": email, "reason": "invalid email"}
            )
            continue
        if not consent:
            rejected.append(
                {"index": index, "email": email, "reason": "missing consent"}
            )
            continue
        if source not in ALLOWED_SOURCES:
            rejected.append(
                {
                    "index": index,
                    "email": email,
                    "reason": f"disallowed source: {source or 'unknown'}",
                }
            )
            continue

        domain = email.rsplit("@", 1)[-1]
        if allowed_domains and domain not in allowed_domains:
            rejected.append(
                {
                    "index": index,
                    "email": email,
                    "reason": f"domain {domain} not in allowlist",
                }
            )
            continue

        accepted.append(
            {
                "email": email,
                "source": source,
                "consent": True,
            }
        )

    output = {
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "contacts": accepted,
        "rejected": rejected,
    }
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
