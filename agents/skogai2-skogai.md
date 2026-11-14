# AGENTS.md

Guidance for coding agents working in this repository. `CLAUDE.md` only links here.

- @SKOGAI.md

Orchestration layer: where skogix and Claude plan and delegate. Stack: bash + mise + jq/yq + argc (tools pinned in `mise.toml`).
Delegation to sub-agents across isolated worktrees and panes is governed by native `herdr` CLI rules documented in `orchestration/README.md`.

## Commands

- Tests: `.harness/init.sh smoke_test` (bash -n, jq parse) / `full_test` (adds `bats -r tests/unit` once tests exist)
- Lint/format (hk, `hk.pkl`): `hk check --all` / `hk fix --all` — shellcheck, shfmt `-i 2 -ci`, private-key and merge-conflict detection. `dash-skogai/tmp/docs/**` is vendored and excluded.
- dash: `mise run dash:check [dot]` (read-only agent check), `mise run dash:graph` (regenerates `dash-skogai/README.md`)

## Layout

- `orchestration/`: the Herdr agent orchestration hub and work order management system. Read `orchestration/AGENTS.md` and `orchestration/README.md`. Orchestrators plan, delegate, and supervise sub-agents here using native `herdr` CLI commands.
- `dash-skogai/`: the skogai type system and `argc config` CLI. Has its own `AGENTS.md`; read it before working there. Its `README.md` is generated from `type/*.md`, never hand-edited.
- herdr oversight (what every agent is doing, its last answer, sending it text): `dash-skogai/type/tool/herdr.md`.
- `.skogai/`: local rules, memory (index `.skogai/memory/MEMORY.md`), scripts, task templates. Check memory before re-deciding things.
- `tmp/`, `.skogai/logs/`: throwaway, gitignored.

## Agent instructions

Instructions live in `AGENTS.md`; every `CLAUDE.md` is only `@AGENTS.md`. See `.skogai/rules/agents-md.md`.

## Harness

vv-harness, re-initialised 2026-11-05; features list reset 2026-11-06 (protocol/probe work removed). Features: `.harness/features.json`; decisions: `.harness/context_summary.md` (read at session start); handoff: `.harness/claude-progress.txt`; build/test: `.harness/init.sh [smoke_test|full_test|focused_test <file>]`; gates: `.claude/hooks/`.

## Git

Identity: Emil Skogsund <emil@skogsund.se>, default SSH key (Skogix). Remote is HTTPS, so the credential helper decides the pushing account. One command per Bash call: chains defeat narrow permission rules, and the commit-gate hook rejects `git add` + `git commit` in one call.

<!-- trail:start -->
## Trail — repo context graph

This repo is indexed in `.trail/cache/`: small linked markdown nodes that explain each
system and carry exact file:line spans, kept in sync with the code through git.

For ANY task here — understanding how something works, finding where code lives,
or scoping a change — get context from the graph before grepping or opening
source files. Re-ask freely (it's cheap) and reuse literal identifiers you
already have (symbol, error string, file name) as the query. New to this repo?
Run `trail map` first — a token-budgeted orientation (dir clusters, hubs,
hotspots), no LLM, no key.

- Run `trail ask "<your question>" --source` → ranked nodes with the relevant
  code spans inlined (each hit's ≤8-line crux by default; `--full` for whole
  definitions when the crux isn't enough). Match the tool to the task shape:
  for understanding or editing, the top node IS the answer — cite its
  `covers:` file:line spans and edit straight from `--source`. For
  exhaustive tasks ("every occurrence / every caller of this pattern"), ranked
  results are top-N, not complete — run `trail grep "<literal>"` instead
  (exhaustive over indexed files, grouped by enclosing symbol), falling back
  to raw `grep -rn` only for unindexed files.
- `trail skeleton <file>` → every definition's signature + span, ~10× cheaper
  than reading the file; use it to skim an API surface.
- `trail callers <symbol>` gives precomputed, exact edges — who calls this.
  Add `--direction out` for what it calls, or `--depth N` to walk
  transitively for the full blast radius. For structural questions, skip
  ranking and use this directly.
- Or browse: `.trail/cache/INDEX.md` lists every node; follow the links.
- Monorepos and folders of multiple repos rank fairly across sub-projects —
  hits carry `[scope/]` labels naming which one they're from. Narrow with
  `trail ask "<task>" --in <scope>/` once you know where you're working.

If a returned span is truncated ("+N more lines"), open the file at that exact
range before finalizing. Only open source files when a node genuinely lacks a
needed detail, and then at the exact file:line the node points to — never
re-read whole files.

After big code changes, refresh the graph with `trail build` (deterministic,
no API key, $0).
<!-- trail:end -->
