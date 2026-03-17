#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  bash instruments/strategy/score.sh key=value ...

Keys:
  compliance consent demand speed margin repeatability automation
  capital_efficiency resilience strategic_fit

Scores must be numbers from 0 to 5. Any missing score defaults to 3.
Ideas with compliance < 4 or consent < 4 are automatically rejected.
EOF
  exit 0
fi

python3 - "$@" <<'PY'
import sys

defaults = {
    "compliance": 3.0,
    "consent": 3.0,
    "demand": 3.0,
    "speed": 3.0,
    "margin": 3.0,
    "repeatability": 3.0,
    "automation": 3.0,
    "capital_efficiency": 3.0,
    "resilience": 3.0,
    "strategic_fit": 3.0,
}

weights = {
    "compliance": 2.0,
    "consent": 1.6,
    "demand": 1.4,
    "speed": 1.1,
    "margin": 1.1,
    "repeatability": 1.0,
    "automation": 1.0,
    "capital_efficiency": 0.9,
    "resilience": 0.9,
    "strategic_fit": 1.2,
}

scores = defaults.copy()
for raw in sys.argv[1:]:
    if "=" not in raw:
        raise SystemExit(f"Invalid argument: {raw!r}. Expected key=value.")
    key, value = raw.split("=", 1)
    if key not in scores:
        allowed = ", ".join(sorted(scores))
        raise SystemExit(f"Unknown key: {key!r}. Allowed keys: {allowed}")
    try:
        numeric = float(value)
    except ValueError as exc:
        raise SystemExit(f"Score for {key!r} must be numeric.") from exc
    if not 0.0 <= numeric <= 5.0:
        raise SystemExit(f"Score for {key!r} must be between 0 and 5.")
    scores[key] = numeric

gates_passed = scores["compliance"] >= 4.0 and scores["consent"] >= 4.0
weighted_total = sum(scores[key] * weights[key] for key in weights)
max_total = 5.0 * sum(weights.values())
percent = (weighted_total / max_total) * 100.0

if not gates_passed:
    recommendation = "REJECT"
elif percent >= 85.0:
    recommendation = "LAUNCH"
elif percent >= 70.0:
    recommendation = "INCUBATE"
elif percent >= 55.0:
    recommendation = "RESEARCH"
else:
    recommendation = "REJECT"

print("Strategy opportunity score")
print("==========================")
for key in sorted(scores):
    print(f"{key:18s}: {scores[key]:.1f}")

print()
print(f"hard_gates_passed : {'yes' if gates_passed else 'no'}")
print(f"weighted_score    : {percent:.1f}/100")
print(f"recommendation    : {recommendation}")

if not gates_passed:
    print()
    print("Reason: ideas with weak compliance or consent should be discarded or redesigned.")
elif recommendation == "LAUNCH":
    print()
    print("Next step: define offer, channel, telemetry, and contingency plan, then run a constrained pilot.")
elif recommendation == "INCUBATE":
    print()
    print("Next step: tighten demand evidence and scope a faster pilot before larger investment.")
elif recommendation == "RESEARCH":
    print()
    print("Next step: collect stronger demand, pricing, or delivery evidence before launch.")
else:
    print()
    print("Next step: redesign or remove the opportunity from the active queue.")
PY
