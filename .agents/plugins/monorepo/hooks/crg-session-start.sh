#!/usr/bin/env bash
# code-review-graph: session start status (Antigravity hook)
set -euo pipefail

cat > /dev/null || true

if ! command -v code-review-graph >/dev/null 2>&1; then
  echo '{}'
  exit 0
fi

msg="$(code-review-graph status --repo "/home/skogix/Work" 2>/dev/null | head -n 1 || true)"
if [ -z "$msg" ]; then
  echo '{}'
  exit 0
fi

CRG_MSG="$msg" python3 -c '
import json, os
m = os.environ.get("CRG_MSG", "")
print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": m}}]}))
' 2>/dev/null || echo '{}'
exit 0
