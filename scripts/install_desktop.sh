#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
DESKTOP_TEMPLATE="${ROOT_DIR}/desktop/Jarvis-Ultra.desktop"
APPLICATIONS_DIR="${HOME}/.local/share/applications"
DESKTOP_DIR="${HOME}/Desktop"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3 first."
  exit 1
fi

mkdir -p "${APPLICATIONS_DIR}"

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install -r "${ROOT_DIR}/requirements.txt"

LAUNCHER="${ROOT_DIR}/scripts/run_jarvis.sh"
DESKTOP_FILE="${APPLICATIONS_DIR}/jarvis-ultra.desktop"

sed \
  -e "s|__JARVIS_EXEC__|${LAUNCHER}|g" \
  -e "s|__JARVIS_PATH__|${ROOT_DIR}|g" \
  "${DESKTOP_TEMPLATE}" > "${DESKTOP_FILE}"

chmod +x "${DESKTOP_FILE}" "${LAUNCHER}"

if [[ -d "${DESKTOP_DIR}" ]]; then
  cp "${DESKTOP_FILE}" "${DESKTOP_DIR}/jarvis-ultra.desktop"
  chmod +x "${DESKTOP_DIR}/jarvis-ultra.desktop"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "${APPLICATIONS_DIR}" >/dev/null 2>&1 || true
fi

echo "Jarvis Ultra desktop app setup complete."
echo "- Menu entry: ${DESKTOP_FILE}"
if [[ -d "${DESKTOP_DIR}" ]]; then
  echo "- Desktop shortcut: ${DESKTOP_DIR}/jarvis-ultra.desktop"
fi
