#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${REPO_ROOT}/frontend"

if [[ ! -d node_modules ]]; then
  npm install
fi

npm run build
exec npm run preview
