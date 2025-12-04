#!/usr/bin/env bash
set -euo pipefail

########################################
# USER CONFIG – EDIT HERE
########################################

# "latest": fetch up to 1000 candles in a single request
# "range" : automatically paginate across the full time window
MODE="range"

# Symbol & interval
SYMBOL="BTCUSDT"
INTERVAL="15m"

# Number of candles per request (max 1000 according to Binance)
LIMIT=1000

# Time in UTC, format: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
START="2025-01-01 00:00:00"
END="2025-12-02 00:00:00"

# Output file name (if empty, auto-generated)
OUTPUT="btcusdt_15m_2025_full.csv"

# Python & virtualenv (optional)
PYTHON_BIN="python"
USE_VENV=true
VENV_PATH=".venv"

########################################
# DO NOT EDIT BELOW UNLESS YOU KNOW WHAT YOU ARE DOING
########################################

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_ROOT}"

if [ "${USE_VENV}" = true ] && [ -d "${VENV_PATH}" ]; then
  # shellcheck disable=SC1090
  source "${VENV_PATH}/bin/activate"
fi

if command -v binance-collector >/dev/null 2>&1; then
  CLI_CMD=(binance-collector)
else
  export PYTHONPATH="src:${PYTHONPATH:-}"
  CLI_CMD=("${PYTHON_BIN}" -m binance_collector)
fi

case "${MODE}" in
  latest)
    ARGS=(latest --symbol "${SYMBOL}" --interval "${INTERVAL}" --limit "${LIMIT}")
    if [ -n "${START}" ]; then
      ARGS+=(--start "${START}")
    fi
    if [ -n "${END}" ]; then
      ARGS+=(--end "${END}")
    fi
    if [ -n "${OUTPUT}" ]; then
      ARGS+=(--output "${OUTPUT}")
    fi
    ;;
  range)
    ARGS=(range --symbol "${SYMBOL}" --interval "${INTERVAL}" --limit "${LIMIT}" \
      --start "${START}" --end "${END}")
    if [ -n "${OUTPUT}" ]; then
      ARGS+=(--output "${OUTPUT}")
    fi
    ;;
  *)
    echo "Invalid MODE: ${MODE}. Supported values: 'latest' or 'range'."
    exit 1
    ;;
esac

echo "Running:" "${CLI_CMD[@]}" "${ARGS[@]}"
echo

"${CLI_CMD[@]}" "${ARGS[@]}"


