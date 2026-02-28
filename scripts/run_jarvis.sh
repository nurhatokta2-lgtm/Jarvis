#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[Jarvis] Python environment not found at ${VENV_DIR}."
  echo "[Jarvis] Run scripts/install_desktop.sh first."
  exit 1
fi

source "${VENV_DIR}/bin/activate"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

cd "${ROOT_DIR}"
uvicorn app.main:app --host "${HOST}" --port "${PORT}" > "${ROOT_DIR}/jarvis.log" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 60); do
  if curl -fsS "http://${HOST}:${PORT}/api/health" >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

APP_URL="http://${HOST}:${PORT}"

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "${APP_URL}" >/dev/null 2>&1 || true
elif command -v open >/dev/null 2>&1; then
  open "${APP_URL}" >/dev/null 2>&1 || true
fi

wait "${SERVER_PID}"
