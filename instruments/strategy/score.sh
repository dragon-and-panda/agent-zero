#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  score.sh "idea text"
  echo "idea text" | score.sh

Scores an opportunity on a small set of autonomy-friendly dimensions and emits
GO, HOLD, or REJECT. Hard-stop patterns reject privacy-invasive or high-risk
missions before any build or launch work begins.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -gt 0 ]]; then
  idea="$*"
else
  idea="$(cat)"
fi

idea="$(printf '%s' "$idea" | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
normalized="$(printf '%s' "$idea" | tr '[:upper:]' '[:lower:]')"

if [[ -z "$normalized" ]]; then
  echo "decision=HOLD"
  echo "score=0"
  echo "reason=No opportunity text provided."
  exit 0
fi

reject_patterns=(
  "sell email list"
  "sell email lists"
  "broker email list"
  "buy email list"
  "scrape inbox"
  "harvest emails"
  "harvest email"
  "spam campaign"
  "unsolicited bulk email"
  "phishing"
  "impersonat"
)

hold_patterns=(
  "forex"
  "trading"
  "securities"
  "investment fund"
  "crypto bot"
)

for pattern in "${reject_patterns[@]}"; do
  if [[ "$normalized" == *"$pattern"* ]]; then
    echo "decision=REJECT"
    echo "score=-100"
    echo "reason=Rejected by compliance gate: privacy-invasive, deceptive, or spam-oriented pattern detected ($pattern)."
    exit 0
  fi
done

score=0
notes=()

add_points() {
  local points="$1"
  local note="$2"
  score=$((score + points))
  notes+=("$note")
}

if [[ "$normalized" == *"consent"* || "$normalized" == *"opt-in"* || "$normalized" == *"authorized"* ]]; then
  add_points 25 "Strong consent or authorization signal."
fi

if [[ "$normalized" == *"service"* || "$normalized" == *"audit"* || "$normalized" == *"cleanup"* || "$normalized" == *"crm"* ]]; then
  add_points 20 "Looks like an operational service with near-term monetization."
fi

if [[ "$normalized" == *"template"* || "$normalized" == *"course"* || "$normalized" == *"tutorial"* || "$normalized" == *"newsletter"* ]]; then
  add_points 15 "Supports reusable product or audience asset creation."
fi

if [[ "$normalized" == *"automation"* || "$normalized" == *"agent"* || "$normalized" == *"workflow"* ]]; then
  add_points 15 "Good automation leverage."
fi

if [[ "$normalized" == *"public data"* || "$normalized" == *"first-party"* || "$normalized" == *"owner-authorized"* ]]; then
  add_points 15 "Data-source posture appears safer."
fi

if [[ "$normalized" == *"retainer"* || "$normalized" == *"subscription"* || "$normalized" == *"recurring"* ]]; then
  add_points 10 "Potential recurring revenue signal."
fi

for pattern in "${hold_patterns[@]}"; do
  if [[ "$normalized" == *"$pattern"* ]]; then
    add_points -20 "Regulated or capital-risk keyword detected ($pattern); requires finance policy pack."
  fi
done

decision="HOLD"
reason="Needs stronger proof of consent, product clarity, or risk controls."

if (( score >= 60 )); then
  decision="GO"
  reason="Meets baseline for a lawful, automatable revenue experiment."
elif (( score >= 25 )); then
  decision="HOLD"
  reason="Promising, but missing enough detail for launch approval."
fi

printf 'decision=%s\n' "$decision"
printf 'score=%s\n' "$score"
printf 'reason=%s\n' "$reason"

if ((${#notes[@]} > 0)); then
  printf 'notes=%s\n' "$(IFS=' | '; echo "${notes[*]}")"
fi
