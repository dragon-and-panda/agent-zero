#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required."
  exit 1
fi

python3 -m venv .venv >/dev/null 2>&1 || true
# shellcheck disable=SC1091
source .venv/bin/activate

python3 -m pip install --upgrade pip >/dev/null
#
# Install *minimal* dependencies for the Survey Helper only.
# (Installing the full Agent Zero requirements may require extra build tooling on some systems.)
#
python3 -m pip install "beautifulsoup4==4.12.3" "playwright==1.49.0"

# Ensure Playwright browser is installed (Chromium)
python3 -m playwright install chromium

echo "Starting Survey Helper GUI..."
python3 run_survey_helper_gui.py

