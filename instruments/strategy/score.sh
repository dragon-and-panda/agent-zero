#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 10 ]]; then
  echo "usage: $0 legality consent provenance platform_risk time_to_cash margin repeatability automation defensibility reversibility" >&2
  echo "values: low medium high" >&2
  exit 2
fi

normalize() {
  local raw="${1,,}"
  case "$raw" in
    low|medium|high)
      printf '%s' "$raw"
      ;;
    *)
      echo "invalid value: $1 (expected low|medium|high)" >&2
      exit 2
      ;;
  esac
}

score() {
  case "$1" in
    low) echo 0 ;;
    medium) echo 1 ;;
    high) echo 2 ;;
  esac
}

legality="$(normalize "$1")"
consent="$(normalize "$2")"
provenance="$(normalize "$3")"
platform_risk="$(normalize "$4")"
time_to_cash="$(normalize "$5")"
margin="$(normalize "$6")"
repeatability="$(normalize "$7")"
automation="$(normalize "$8")"
defensibility="$(normalize "$9")"
reversibility="$(normalize "${10}")"

# Hard gates: reject any lane that is not clearly lawful, consensual,
# provenance-clean, and compatible with platform terms.
if [[ "$legality" != "high" || "$consent" != "high" || "$provenance" != "high" ]]; then
  echo "REJECT"
  exit 0
fi

if [[ "$platform_risk" == "low" || "$reversibility" == "low" ]]; then
  echo "REJECT"
  exit 0
fi

soft_factors=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility" "$reversibility")
high_count=0
for factor in "${soft_factors[@]}"; do
  if [[ "$factor" == "low" ]]; then
    echo "HOLD"
    exit 0
  fi
  if [[ "$factor" == "high" ]]; then
    ((high_count+=1))
  fi
done

if (( high_count >= 3 )) && [[ "$platform_risk" == "high" ]]; then
  echo "PASS"
else
  echo "HOLD"
fi
