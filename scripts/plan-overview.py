#!/usr/bin/env python3
"""Size of the plan: every skogai/monorepo issue as one row, for the plan dashboard.

Reads the issues with `gh issue list` and writes JSON `{rows, meta}`:
one row per issue with its milestone, size label, points, target repos
(from the body's **Repo:**/**Repos:**/**Where:** line) and the open issues
it is blocked by (from "Blocked by #n"). Prints a short summary to stderr.

Sizes are GitHub labels (`size: S`, `size: M`, `size: L`), so change them on
the issue. Points: S=1, M=3, L=8. `owner decision` marks issues that wait on
the owner.

usage: plan-overview.py [OUT]   (default .skogai/tmp/plan-overview.json)
"""
import json, re, subprocess, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = "skogai/monorepo"
POINTS = {"S": 1, "M": 3, "L": 8}
out = Path(sys.argv[1] if len(sys.argv) > 1 else ".skogai/tmp/plan-overview.json")

issues = json.loads(subprocess.check_output([
    "gh", "issue", "list", "-R", REPO, "--state", "all", "--limit", "500",
    "--json", "number,title,state,milestone,labels,body,createdAt,closedAt,url"]))
state = {i["number"]: i["state"] for i in issues}


def targets(body):
    """Repos named on the body's Repo/Repos/Where line, as owner/name."""
    m = re.search(r"\*\*(?:Repos?|Where):\*\*([^\n]*)", body or "")
    if not m:
        return ["skogai/monorepo"]
    line = m.group(1)
    found = re.findall(r"\b(skogai2?/[A-Za-z0-9._-]+?)(?=[\s,.;()`]|$)", line)
    if found:
        return sorted(set(found))
    if re.search(r"workstation|home mise config|~/\.", line):
        return ["workstation"]
    if "across repos" in line:
        return ["several repos"]
    return ["skogai/monorepo"]


rows = []
for i in sorted(issues, key=lambda i: i["number"]):
    labels = [l["name"] for l in i["labels"]]
    size = next((l.split(": ", 1)[1] for l in labels if l.startswith("size: ")), None)
    blocked = sorted({int(n) for b in re.findall(r"Blocked by ([^.\n]*)", i["body"] or "")
                      for n in re.findall(r"#(\d+)", b)})
    open_blockers = [n for n in blocked if state.get(n) == "OPEN"]
    ms = (i["milestone"] or {}).get("title") or "Backlog"
    rows.append({
        "number": i["number"],
        "title": i["title"],
        "state": i["state"].lower(),
        "milestone": ms,
        "track": "Pathfinder" if re.match(r"U\d+:", ms) else ("mise toolkit" if ms.startswith("mise toolkit") else "Backlog"),
        "size": size,
        "points": POINTS.get(size, 0),
        "decision": "owner decision" in labels,
        "repos": "; ".join(targets(i["body"])),
        "blocked_by": " ".join(f"#{n}" for n in open_blockers),
        "ready": i["state"] == "OPEN" and not open_blockers and "owner decision" not in labels,
        "created": i["createdAt"][:10],
        "closed": (i["closedAt"] or "")[:10],
        "url": i["url"],
    })

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
meta = [
    {"label": "Generated", "value": now},
    {"label": "Input", "value": f"gh issue list -R {REPO} --state all"},
    {"label": "plan-overview.py", "value": Path(__file__).read_text(), "type": "code", "lang": "python"},
]
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"rows": rows, "meta": meta}, ensure_ascii=False, indent=1))

o = [r for r in rows if r["state"] == "open"]
by = Counter()
for r in o:
    by[r["milestone"]] += r["points"]
print(f"{len(o)} open issues, {sum(r['points'] for r in o)} points, "
      f"{sum(r['ready'] for r in o)} ready, {sum(r['decision'] for r in o)} owner decisions -> {out}", file=sys.stderr)
for k, v in sorted(by.items(), key=lambda kv: -kv[1]):
    print(f"  {v:3d}  {k}", file=sys.stderr)
