#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 [--idea TEXT] --legality VALUE --consent VALUE --provenance VALUE --tos VALUE --time VALUE --margin VALUE --repeatability VALUE --automation VALUE --defensibility VALUE" >&2
  echo "values must be low|medium|high" >&2
}

normalize() {
  local value="$1"
  case "$value" in
    low|medium|high)
      printf '%s' "$value"
      ;;
    *)
      echo "invalid value: $value" >&2
      exit 1
      ;;
  esac
}

idea=""
legality=""
consent=""
provenance=""
tos_conflict=""
time_to_cash=""
margin=""
repeatability=""
automation=""
defensibility=""

if [[ $# -eq 9 ]]; then
  legality="$(normalize "$1")"
  consent="$(normalize "$2")"
  provenance="$(normalize "$3")"
  tos_conflict="$(normalize "$4")"
  time_to_cash="$(normalize "$5")"
  margin="$(normalize "$6")"
  repeatability="$(normalize "$7")"
  automation="$(normalize "$8")"
  defensibility="$(normalize "$9")"
else
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --idea)
        idea="${2:-}"
        shift 2
        ;;
      --legality)
        legality="$(normalize "${2:-}")"
        shift 2
        ;;
      --consent)
        consent="$(normalize "${2:-}")"
        shift 2
        ;;
      --provenance)
        provenance="$(normalize "${2:-}")"
        shift 2
        ;;
      --tos)
        tos_conflict="$(normalize "${2:-}")"
        shift 2
        ;;
      --time)
        time_to_cash="$(normalize "${2:-}")"
        shift 2
        ;;
      --margin)
        margin="$(normalize "${2:-}")"
        shift 2
        ;;
      --repeatability)
        repeatability="$(normalize "${2:-}")"
        shift 2
        ;;
      --automation)
        automation="$(normalize "${2:-}")"
        shift 2
        ;;
      --defensibility)
        defensibility="$(normalize "${2:-}")"
        shift 2
        ;;
      *)
        usage
        exit 1
        ;;
    esac
  done

  required=(
    "$legality"
    "$consent"
    "$provenance"
    "$tos_conflict"
    "$time_to_cash"
    "$margin"
    "$repeatability"
    "$automation"
    "$defensibility"
  )

  for value in "${required[@]}"; do
    if [[ -z "$value" ]]; then
      usage
      exit 1
    fi
  done
fi

if [[ "$legality" == "low" || "$consent" == "low" || "$provenance" == "low" || "$tos_conflict" == "low" ]]; then
  if [[ -n "$idea" ]]; then
    echo "Lane: $idea"
  fi
  echo "REJECT: failed hard gate (legality, consent, provenance, or platform terms)."
  exit 0
fi

if [[ "$legality" == "medium" || "$consent" == "medium" || "$provenance" == "medium" || "$tos_conflict" == "medium" ]]; then
  if [[ -n "$idea" ]]; then
    echo "Lane: $idea"
  fi
  echo "HOLD: requires legal or operator review before activation."
  exit 0
fi

soft_values=("$time_to_cash" "$margin" "$repeatability" "$automation" "$defensibility")
for value in "${soft_values[@]}"; do
  if [[ "$value" == "low" ]]; then
    if [[ -n "$idea" ]]; then
      echo "Lane: $idea"
    fi
    echo "HOLD: compliant idea, but execution factors are not yet strong enough."
    exit 0
  fi
done

if [[ -n "$idea" ]]; then
  echo "Lane: $idea"
fi
echo "PASS: compliant and operationally attractive."
