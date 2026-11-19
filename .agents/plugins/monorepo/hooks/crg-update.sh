#!/usr/bin/env bash
# code-review-graph: incremental update after file writes/edits (Antigravity hook)
set -euo pipefail

cat > /dev/null || true

if command -v code-review-graph >/dev/null 2>&1; then
  code-review-graph update --skip-flows --repo "/home/skogix/Work" >/dev/null 2>&1 || true
fi
echo '{}'
exit 0
