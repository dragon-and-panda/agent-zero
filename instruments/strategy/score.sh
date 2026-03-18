#!/bin/bash
set -euo pipefail

if [[ $# -gt 0 ]]; then
  INPUT="$*"
else
  INPUT="$(python3 -c 'import sys; print(sys.stdin.read())')"
fi

if [[ -z "${INPUT// }" ]]; then
  echo "Usage: bash /workspace/instruments/strategy/score.sh \"opportunity summary\""
  exit 1
fi

OPPORTUNITY="$INPUT" python3 - <<'PY'
import os
import re

text = os.environ["OPPORTUNITY"].strip()
normalized = text.lower()

reject_patterns = {
    "private email list resale": r"((sell|broker|rent).*(email list|contact list|list of emails|email addresses?|contacts?))|((email list|contact list|list of emails|email addresses?|contacts?).*(sell|broker|rent))",
    "mailbox harvesting": r"((harvest|scrape|extract).*(gmail|google mail|mailbox|inbox|sent|cc|email addresses?|contacts?))|((gmail|google mail|mailbox|inbox|sent|cc).*(harvest|scrape|extract))",
    "spam or bulk unsolicited outreach": r"\bspam\b|bulk unsolicited|cold blast|mass outreach",
    "anti-bot or captcha evasion": r"captcha|anti-bot|evad(e|ing)|bypass",
}

hold_patterns = {
    "speculative trading": r"forex|fx trading|leverag|day trading|speculative trading",
    "unapproved funds routing": r"cash app|venmo|personal account|wallet",
}

positive_patterns = {
    "consent": r"consent|opt[- ]in|authorized|customer[- ]owned|permission",
    "service": r"service|consult|cleanup|ops|implementation|retainer",
    "product": r"template|course|tutorial|playbook|guide|prompt pack",
    "public data": r"public data|public business|directory|market research|competitor",
    "listing": r"listing|marketplace|resale|seller",
    "redundancy": r"redundan|backup|fallback|contingen",
}

reject_hits = [name for name, pattern in reject_patterns.items() if re.search(pattern, normalized)]
hold_hits = [name for name, pattern in hold_patterns.items() if re.search(pattern, normalized)]
positive_hits = [name for name, pattern in positive_patterns.items() if re.search(pattern, normalized)]

scores = {
    "legality": 5,
    "consent": 3 if "consent" in positive_hits else 2,
    "capital_efficiency": 5,
    "durability": 2,
    "operational_risk": 3,
}

if reject_hits:
    scores["legality"] = 0
    scores["consent"] = 0
    scores["operational_risk"] = 0

if hold_hits:
    scores["capital_efficiency"] = min(scores["capital_efficiency"], 1)
    scores["operational_risk"] = min(scores["operational_risk"], 1)

if "service" in positive_hits:
    scores["durability"] += 1
if "product" in positive_hits:
    scores["durability"] += 1
if "redundancy" in positive_hits:
    scores["operational_risk"] += 1
if "listing" in positive_hits or "public data" in positive_hits:
    scores["durability"] += 1

scores["durability"] = min(scores["durability"], 5)
scores["operational_risk"] = min(scores["operational_risk"], 5)

total = sum(scores.values())

if reject_hits:
    status = "REJECT"
    action = "Do not execute. Replace with a consent-based offer or public-data workflow."
elif hold_hits:
    status = "HOLD"
    action = "Document controls, fallback paths, and risk limits before reconsidering."
elif total >= 18:
    status = "GO"
    action = "Proceed to scoping, pricing, and a smallest viable test."
else:
    status = "HOLD"
    action = "Strengthen consent, offer clarity, or redundancy before launch."

print(f"Opportunity: {text}")
print(f"Status: {status}")
print("Scores:")
for key, value in scores.items():
    print(f"  - {key}: {value}/5")
print(f"Total: {total}/25")
print("Signals:")
if reject_hits:
    for hit in reject_hits:
        print(f"  - reject: {hit}")
if hold_hits:
    for hit in hold_hits:
        print(f"  - hold: {hit}")
if positive_hits:
    for hit in positive_hits:
        print(f"  - positive: {hit}")
print(f"Recommended action: {action}")
PY
