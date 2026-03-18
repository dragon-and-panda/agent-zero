#!/usr/bin/env bash
set -euo pipefail

name="Unnamed idea"
legality="medium"
consent="medium"
margin="medium"
speed="medium"
automation="medium"
defensibility="medium"
redundancy="medium"
privacy_invasive="no"

usage() {
    cat <<'EOF'
Usage:
  score.sh --name NAME [factor flags]

Factors accept: low, medium, high
Flags:
  --legality VALUE
  --consent VALUE
  --margin VALUE
  --speed VALUE
  --automation VALUE
  --defensibility VALUE
  --redundancy VALUE
  --privacy-invasive yes|no
EOF
}

to_points() {
    case "$1" in
        low) echo 1 ;;
        medium) echo 2 ;;
        high) echo 3 ;;
        *)
            echo "Invalid value: $1" >&2
            exit 1
            ;;
    esac
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)
            name="$2"
            shift 2
            ;;
        --legality)
            legality="$2"
            shift 2
            ;;
        --consent)
            consent="$2"
            shift 2
            ;;
        --margin)
            margin="$2"
            shift 2
            ;;
        --speed)
            speed="$2"
            shift 2
            ;;
        --automation)
            automation="$2"
            shift 2
            ;;
        --defensibility)
            defensibility="$2"
            shift 2
            ;;
        --redundancy)
            redundancy="$2"
            shift 2
            ;;
        --privacy-invasive)
            privacy_invasive="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [[ "$privacy_invasive" != "yes" && "$privacy_invasive" != "no" ]]; then
    echo "Invalid value for --privacy-invasive: $privacy_invasive" >&2
    exit 1
fi

if [[ "$legality" == "low" || "$consent" == "low" || "$privacy_invasive" == "yes" ]]; then
    echo "Idea: $name"
    echo "Recommendation: REJECT"
    echo "Reason: failed hard-gate on legality, consent, or privacy handling"
    exit 0
fi

score=0
score=$((score + $(to_points "$legality") * 3))
score=$((score + $(to_points "$consent") * 3))
score=$((score + $(to_points "$margin") * 2))
score=$((score + $(to_points "$speed") * 2))
score=$((score + $(to_points "$automation") * 2))
score=$((score + $(to_points "$defensibility") * 2))
score=$((score + $(to_points "$redundancy") * 1))

recommendation="HOLD"
if (( score >= 32 )); then
    recommendation="GO"
elif (( score <= 22 )); then
    recommendation="REJECT"
fi

echo "Idea: $name"
echo "Legality: $legality"
echo "Consent: $consent"
echo "Margin: $margin"
echo "Speed: $speed"
echo "Automation: $automation"
echo "Defensibility: $defensibility"
echo "Redundancy: $redundancy"
echo "Privacy invasive: $privacy_invasive"
echo "Weighted score: $score"
echo "Recommendation: $recommendation"
