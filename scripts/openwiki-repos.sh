#!/usr/bin/env bash
# Print "<name> <url>" for every mani.yaml project tagged `openwiki`: the repos the wiki covers.
# With --clone, also clone each one that is missing into repos/<name> (depth 50).
# A private repo needs credentials: locally your own git credentials, in CI the
# OPENWIKI_REPOS_TOKEN environment variable. A repo that cannot be cloned is reported and skipped.
set -euo pipefail
cd "$(dirname "$0")/.."

list() {
  awk '
    /^projects:/ { p = 1; next }
    /^[a-z]/     { p = 0 }
    p && /^  [A-Za-z0-9._-]+:$/ { name = $1; sub(/:$/, "", name) }
    p && /^    url:/            { url = $2 }
    p && /^    tags:/ && /[\[ ,]openwiki[\], ]/ { print name, url }
  ' mani.yaml
}

if [ "${1:-}" != "--clone" ]; then
  list
  exit 0
fi

auth=()
if [ -n "${OPENWIKI_REPOS_TOKEN:-}" ]; then
  basic=$(printf 'x-access-token:%s' "$OPENWIKI_REPOS_TOKEN" | base64 | tr -d '\n')
  auth=(-c "http.https://github.com/.extraheader=AUTHORIZATION: basic $basic")
fi

failed=0
while read -r name url; do
  if [ -e "repos/$name" ]; then
    echo "present: $name"
  elif GIT_TERMINAL_PROMPT=0 git "${auth[@]}" clone --quiet --depth 50 "$url" "repos/$name"; then
    echo "cloned:  $name"
  else
    echo "FAILED:  $name ($url)" >&2
    rm -rf "repos/$name"
    failed=$((failed + 1))
  fi
done < <(list)
echo "$failed repo(s) could not be cloned"
