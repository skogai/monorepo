# Cache of each repo's root AGENTS.md

Date: 2026-11-14. Run: Claude (claude-sonnet-5-5), Claude Code harness through T3 Code,
machine skogix-workstation, checkout /home/skogix/Work, base 8f6c22d (master, mani catalog, PR #51).

Source observation: `mani.yaml` task `agents-cache` runs in `repos/<name>`, copies the root
`AGENTS.md` to `../../agents/<name>.md`, or deletes that copy when the repo has none. The mise
task `agents:sync` runs `mani sync` and then that task. Decisions by Skogix in the planning
thread: committed cache, filled from clones (no `gh`, no token), no file and delete-stale for a
repo without AGENTS.md, refresh by hand.

Machine prerequisites: mise with mani 0.32.1 (pinned in mise.toml), git, network, and git
access to the five repos under github.com/skogai (cloning used the machine's gh credential helper).
The cache covers only repos cloned on the machine that refreshes. Not run: a fresh machine,
a remote container, a private-repo clone without credentials, a repo removed from mani.yaml
(its file would be left as an orphan).

| Command | Expected | Actual | Verdict | Next action |
|---|---|---|---|---|
| `mise run agents:sync` | Five repos cloned; two cached, three reported without AGENTS.md | mise-plugin and skogai-jq cached; skogai, skogai-core, skogix reported "no AGENTS.md" | pass | Commit the cache |
| `ls agents` | `mise-plugin.md skogai-jq.md` | As expected | pass | none |
| `for n in mise-plugin skogai-jq; do cmp repos/$n/AGENTS.md agents/$n.md && echo ok:$n; done` | Identical files | ok for both | pass | none |
| `echo x > agents/skogix.md; mani run agents-cache --all --ignore-non-existing; test ! -e agents/skogix.md` | Stale copy removed | Removed | pass | none |
| second `mise run agents:sync` after the cache commit (in a fresh worktree with its own clones), then `git status --short` | Empty | Empty | pass | none |
| `mise tasks ls \| grep agents` | `agents:sync` listed | Listed | pass | none |
