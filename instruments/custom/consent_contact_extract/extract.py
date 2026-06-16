import argparse
import csv
import pathlib
import re
import sys


EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract consented contact emails from owner-authorized files."
    )
    parser.add_argument("--input", action="append", required=True, help="Input file path")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument(
        "--owner-authorized",
        required=True,
        choices=("yes", "no"),
        help="Must be yes to proceed",
    )
    parser.add_argument(
        "--consent-basis",
        required=True,
        choices=("opted_in", "existing_customer", "contractual", "other_documented_basis"),
        help="Lawful basis for first-party processing",
    )
    parser.add_argument(
        "--domain-allowlist",
        action="append",
        default=[],
        help="Optional domain filter; may be repeated",
    )
    return parser.parse_args()


def iter_emails(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return EMAIL_RE.findall(text)


def main() -> int:
    args = parse_args()

    if args.owner_authorized != "yes":
        print("refusing extraction: owner authorization is required", file=sys.stderr)
        return 2

    allowed_domains = {domain.lower() for domain in args.domain_allowlist}
    seen: set[tuple[str, str]] = set()
    rows: list[dict[str, str]] = []

    for input_path in args.input:
        path = pathlib.Path(input_path)
        if not path.exists():
            print(f"missing input: {path}", file=sys.stderr)
            return 3

        for email in iter_emails(path):
            normalized = email.lower()
            domain = normalized.split("@", 1)[1]
            if allowed_domains and domain not in allowed_domains:
                continue

            key = (normalized, str(path))
            if key in seen:
                continue

            seen.add(key)
            rows.append(
                {
                    "email": normalized,
                    "source_file": str(path),
                    "consent_basis": args.consent_basis,
                }
            )

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["email", "source_file", "consent_basis"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} contacts to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
