#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}/backend"
export PYTHONPATH=.

if [[ -x "${REPO_ROOT}/venv/bin/uvicorn" ]]; then
  exec "${REPO_ROOT}/venv/bin/uvicorn" main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'
fi

if command -v uvicorn >/dev/null 2>&1; then
  exec uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'
fi

echo "uvicorn not found. Run: make install" >&2
exit 1
