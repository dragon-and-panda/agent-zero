#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  score.sh KEY=VALUE ...

Required hard-gate inputs:
  legality=pass|fail
  consent=pass|fail|unknown|unclear
  provenance=pass|fail|unknown|unclear
  tos=pass|fail|unknown|unclear

Required soft-factor inputs:
  time=high|medium|low
  margin=high|medium|low
  repeatability=high|medium|low
  automation=high|medium|low
  defensibility=high|medium|low

Optional:
  notes="free-form text"

Output:
  RESULT=PASS|HOLD|REJECT
  REASON=...
EOF
}

if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

declare -A args=()

for arg in "$@"; do
    if [[ "$arg" != *=* ]]; then
        echo "Invalid argument: $arg" >&2
        usage >&2
        exit 1
    fi
    key="${arg%%=*}"
    value="${arg#*=}"
    args["$key"]="$value"
done

require_arg() {
    local key="$1"
    if [[ -z "${args[$key]:-}" ]]; then
        echo "Missing required arg: $key" >&2
        usage >&2
        exit 1
    fi
}

for key in legality consent provenance tos time margin repeatability automation defensibility; do
    require_arg "$key"
done

is_low() {
    [[ "$1" == "low" ]]
}

reject_reasons=()
hold_reasons=()

if [[ "${args[legality]}" != "pass" ]]; then
    reject_reasons+=("legality gate failed")
fi

for key in consent provenance tos; do
    case "${args[$key]}" in
        pass)
            ;;
        fail)
            reject_reasons+=("$key gate failed")
            ;;
        unknown|unclear)
            hold_reasons+=("$key gate is ${args[$key]}")
            ;;
        *)
            reject_reasons+=("$key gate has invalid value '${args[$key]}'")
            ;;
    esac
done

if [[ "${#reject_reasons[@]}" -gt 0 ]]; then
    echo "RESULT=REJECT"
    echo "REASON=$(IFS='; '; echo "${reject_reasons[*]}")"
    exit 0
fi

if [[ "${#hold_reasons[@]}" -gt 0 ]]; then
    echo "RESULT=HOLD"
    echo "REASON=$(IFS='; '; echo "${hold_reasons[*]}")"
    exit 0
fi

soft_lows=()
for key in time margin repeatability automation defensibility; do
    if is_low "${args[$key]}"; then
        soft_lows+=("$key")
    fi
done

if [[ "${#soft_lows[@]}" -gt 0 ]]; then
    echo "RESULT=HOLD"
    echo "REASON=Soft factors too weak: $(IFS=', '; echo "${soft_lows[*]}")"
    exit 0
fi

echo "RESULT=PASS"
echo "REASON=All hard gates passed and soft factors are viable"
