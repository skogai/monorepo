#!/usr/bin/env bash
# Resolve a code-review-graph target for the crg:* mise tasks.
#   crg-repo.sh <root> <name-or-path>   print the repo directory (exit 1 if not found)
#   crg-repo.sh <root>                  print every repo that already has a graph (root first)
set -eu
root=$1
if [ $# -ge 2 ] && [ -n "$2" ]; then
  if [ -d "$2" ]; then
    (cd "$2" && pwd)
  elif [ -d "$root/repos/$2" ]; then
    printf '%s\n' "$root/repos/$2"
  else
    printf 'Repo not found: %s (not a directory, not under repos/)\n' "$2" >&2
    exit 1
  fi
else
  for repo in "$root" "$root"/repos/*; do
    [ -f "$repo/.code-review-graph/graph.db" ] && printf '%s\n' "$repo"
  done
  exit 0
fi
