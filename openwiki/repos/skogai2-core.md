---
type: repository
title: skogai2-core
description: Bash/argc control plane for the SkogAI repo fleet, copied from skogai/core into the skogai2 org. Work in progress; the root CLI is mostly stubs and a new `repo` module plus a workorder/dispatch design are the live parts.
tags: [control-plane, argc, bash, fleet, dispatch, wip]
repo: skogai2/core
commit: 02619f3
last_commit: 2026-11-09
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-core/Argcfile.sh
  - repos/skogai2-core/bin/skogai
  - repos/skogai2-core/SKOGAI.md
  - repos/skogai2-core/README.md
  - repos/skogai2-core/PLAN.md
  - repos/skogai2-core/FILESTRUCTURE.md
  - repos/skogai2-core/HANDOVER.md
  - repos/skogai2-core/todo.list
  - repos/skogai2-core/.envrc
  - repos/skogai2-core/mise.toml
  - repos/skogai2-core/scripts/bootstrap.sh
  - repos/skogai2-core/scripts/build.sh
  - repos/skogai2-core/scripts/context/context-start.sh
  - repos/skogai2-core/tests/argc-smoke.sh
  - repos/skogai2-core/.config/wt.toml
  - repos/skogai2-core/.skogai/modules/repo/argc.sh
  - repos/skogai2-core/.skogai/modules/repo/module.md
  - repos/skogai2-core/.skogai/modules/repo/schema/entry.json
  - repos/skogai2-core/.skogai/modules/repo/tests/repo.bats
  - repos/skogai2-core/.skogai/repo/repos.toml
  - repos/skogai2-core/.skogai/repo/gita/groups.csv
  - repos/skogai2-core/contracts/inbox-mod.toml
  - repos/skogai2-core/contracts/marketplace.toml
  - repos/skogai2-core/docs/dependencies.md
  - repos/skogai2-core/docs/decisions/0002-resolve-context-script-dir-via-argc-script-path.md
  - repos/skogai2-core/docs/decisions/0003-split-argc-interface-design-from-consumption.md
  - repos/skogai2-core/.ai/cactus/q2-34-revive-skogai-core-in-place-or.md
  - repos/skogai2-core/.github/workflows/openwiki-update.yml
  - repos/skogai2-core/openwiki/.last-update.json
---

# skogai2-core

**The fleet control plane: a Bash/argc `skogai` command for listing, registering and preparing work on SkogAI repositories, plus the design for dispatching workorders to them.** It is a copy of `skogai/core` moved to the `skogai2` org on 2026-10-24 (`HANDOVER.md:11-13`); its own docs still call it `skogai/core`. State: work in progress. Thirteen commits on 2026-10-24 added the handover, contracts and a `repo` module; the last two commits (2026-10-25, 2026-11-09 "WIP") are small. The root `Argcfile.sh` was reduced to stubs on 2026-09-16 and has not been refilled, so most documented commands do nothing at HEAD.

## Source map

| Path | Holds |
|---|---|
| `Argcfile.sh` | Root argc CLI source (225 lines). `scripts/argc/skogai` is a symlink to it. |
| `bin/skogai` | Committed standalone wrapper built from the Argcfile by `argc --argc-build` (2804 lines). Not hand-edited. |
| `SKOGAI.md` | Agent entry point. `AGENTS.md` is a symlink to it; `CLAUDE.md` routes to it. |
| `README.md`, `PLAN.md`, `FILESTRUCTURE.md`, `todo.list` | Overview, direction, file map, backlog. |
| `HANDOVER.md` | 2026-10-24 design: one workorder primitive, registry and dispatch in core. |
| `.skogai/modules/repo/` | The new `repo` module: `argc.sh`, `module.md` (interface), `schema/entry.json`, `tests/repo.bats`. |
| `.skogai/repo/` | Module state: `repos.toml` and gita's `gita/repos.csv`, `gita/groups.csv`. |
| `contracts/` | Draft per-repo environment contracts: `inbox-mod.toml`, `marketplace.toml`. |
| `.ai/cactus/` | 15 decision records (`q1`..`q18`) from the "cactus" question tool, thread `dispatch`. |
| `scripts/` | `bootstrap.sh`, `build.sh`, `context/` (three argc context emitters), `hooks/codex-hook-probe.sh`. |
| `tests/argc-smoke.sh` | Parser smoke test for the root Argcfile. |
| `docs/` | `dependencies.md`, three ADRs in `decisions/`, captured references for argc, gita and worktrunk. |
| `settings/` | Codex config reference, `requirements.txt` (PyYAML, gita). |
| `.claude/`, `.agents/`, `.codex/` | Agent config: two copies of the `skogai-argc` skill, live rules, a codebase map, Codex hooks. |
| `.config/wt.toml`, `.envrc`, `mise.toml` | Worktrunk pre-start hook, direnv activation, mise tool list. |
| `openwiki/` | The repo's own generated wiki (see below). |
| `.github/workflows/` | `claude.yml` (`@claude` mentions), `openwiki-update.yml` (daily wiki refresh). |
| `tmp/` | Scratch output; only `.gitkeep` files are tracked. |

## How it works

### Root CLI (`Argcfile.sh`)

The file declares three namespaces with argc comment tags: `repo`, `marketplace`, `tools`, plus an unfinished `queue`. It requires `gh`, `gita` and `wt` (`Argcfile.sh:22`) and declares its settings as `@env` lines (`Argcfile.sh:7-18`).

At HEAD only four commands have bodies:

- `repo list` runs `gita ls "$GITA_GROUP"` (`Argcfile.sh:35-37`). `todo.list:23` records that this always failed, because `gita ls` takes a repo name and not a group.
- `repo status` runs `gita ll "$GITA_GROUP"` (`Argcfile.sh:45-47`).
- `marketplace update` calls `claude plugin marketplace update` and `codex plugin marketplace update` (`Argcfile.sh:108-113`); the `--no-claude`/`--no-codex` flag tests do not gate anything.
- `tools wt create` wraps `wt switch --create` (`Argcfile.sh:171-177`).

`repo update|add|review|issue|pr|digest` and every `tools claude|codex` command are `:` no-ops. `repo workon`, which `PLAN.md` calls the main orchestration command, is not defined. `queue` and `queue mcp` call `scripts/queue.sb` and `scripts/queue.sh`, neither of which exists.

`bin/skogai` matches this stubbed source (same function list), so the committed wrapper is equally hollow.

### Bootstrap and build

`.envrc` runs `scripts/bootstrap.sh`, activates `.venv`, adds `scripts/argc` to `PATH`, and runs `scripts/build.sh`. Bootstrap checks for `uv`, `git`, and an authenticated `gh`, then installs `settings/requirements.txt` into `.venv`. Build runs `argc --argc-build` twice (to `tmp/bin/skogai` and `bin/skogai`), generates man pages and bash/zsh completions under `tmp/`. `.config/wt.toml:15-19` runs the same bootstrap and build from the Worktrunk `pre-start` hook.

`mise.toml` lists `argc`, `direnv`, `gh`, `uv`, `worktrunk`, but bootstrap does not call mise. `docs/dependencies.md:47-58` records this as an experiment and notes that the worktrunk binary is named `wt`.

### The `repo` module (`.skogai/modules/repo/`)

This is the newer design: `skogai repo` as a module of the modular `skogai` runner, not a namespace of the root Argcfile. `argc.sh` refuses to run without `SKOGAI_MODULE_DIR` (`argc.sh:9`), which the runner sets. It needs `gita`, `yq`, `jq`.

- `list`, `status`: gita, run with `GITA_PROJECT_HOME` pointed at the module's own state directory so `~/.config/gita` is never touched (`argc.sh:38-40`).
- `known`, `show NAME`: the fleet is every row of `gita/repos.csv` merged with every table of `repos.toml`; `repos.toml` wins (`argc.sh:53-78`). `show` prints one `Entry` (`name`, `url`, `path`, `contract`) as JSON matching `schema/entry.json`.
- Config keys `repo.group` (default `src`) and `repo.home` (default `.skogai/repo`), read as `SKOGAI_REPO_GROUP` and `SKOGAI_REPO_HOME`.

`module.md` is the interface contract (signatures, exit codes, state files). `tests/repo.bats` has tests for all four commands and is meant to run through `skogai module test repo`. The module's description names `add` and `workon`; neither is implemented.

Committed state: `repos.toml` adds `core`, `inbox-mod`, `marketplace`; `gita/repos.csv` has 13 rows with absolute paths under `/home/skogix`; `groups.csv` defines groups `src`, `forks`, `home`.

### Workorder and dispatch design (`HANDOVER.md`)

Not implemented here. The handover proposes one primitive, a `WorkOrder` addressed to a human, agent or repo, with a `Result` of `Done | Blocked | Refused | Expired`, stored as files in git (`HANDOVER.md:52-98`). Core would hold the registry (`repos.toml`) and dispatch; each repo would own a `contract` (install, checks, known failures, forbidden actions). `contracts/*.toml` are two drafts of that shape. The first dispatch backend is a herdr pane with a `wt` worktree; cloud agents come later (`HANDOVER.md:136-140`). The `.ai/cactus/q*.md` files record the answers that shaped this.

### Other parts

- `scripts/context/*.sh`: argc scripts that emit a context block for a session, an issue or a PR. They were called by `repo workon`/`repo review`, which are gone or stubbed.
- ADRs: 0002 (resolve script paths with `argc --argc-script-path`, accepted), 0003 (separate interface-design and worker agent roles, proposed).
- `.codex/hooks.json` wires an experimental probe plus two inline pattern checks.

### The repo's own `openwiki/`

`openwiki/` holds six generated pages (architecture, concepts, integrations, testing, two workflows) with `.claims/*.json` evidence files. `openwiki/.last-update.json` says the last run was `init` on 2026-09-20 with status `interrupted`; the folder's last commit is 2026-09-24. It predates the `repo` module, `HANDOVER.md`, `contracts/` and the move to skogai2, so treat it as a description of the September state. `openwiki-update.yml` schedules a daily refresh that opens a PR on branch `openwiki/update`; no later update is in the history. This page was written from source, not from that wiki.

## How to use it

As the files define it (nothing here was run):

- Prerequisites on `PATH`: `argc`, `uv`, `git`, authenticated `gh`, `gita`, `wt`; the module also needs `yq`, `jq` and the `skogai` runner.
- `direnv allow` in the repo triggers bootstrap and build through `.envrc`.
- `argc --argc-eval Argcfile.sh --help`, `bash tests/argc-smoke.sh`, `./scripts/build.sh`, `./bin/skogai repo list` are the commands `SKOGAI.md:74-79` lists.
- Module: `skogai repo list|status|known|show NAME`, `skogai module test repo`, after `skogai module build --to local` (`todo.list:22`).
- Machine assumptions: `Argcfile.sh:7-18` defaults point at `/home/skogix/...` (`DEV_BASE_DIR`, `WORKTREE_DIR`, `SKOGAI_MARKETPLACE_REPO_DIR`, `SKOGAI_CLAUDE_PLUGIN_*`, `SKOGAI_CODEX_PLUGIN_*`). `gita/repos.csv` is machine-specific.
- CI secrets by name: `OPENWIKI_LANGSMITH_API_KEY`, `LANGSMITH_API_KEY` (openwiki workflow).

## Relations to other SkogAI repos

- `skogai/core` (older org): this repo is its copy; the old one stays as git remote `skogai` on the owner's machine (`HANDOVER.md:11-13`, cactus `q2`). `_choice_*` helpers still query the `skogai` org (`Argcfile.sh:184-197`).
- `skogai2-skogai-runner`: provides `skogai module ...`, `skogai config`, and `skogai runner wo`; the `repo` module is built to slot into it and `requires: [core]` (`module.md:7`).
- `skogai2-marketplace`: `marketplace update` syncs it; `contracts/marketplace.toml` is its draft contract; `todo.list:3` treats core as staging for future marketplace plugins.
- `inbox-mod` (cactus): draft contract here; the handover records why its hooks are being dropped.
- `skogai2-skogai`: the handover was written from a session in `~/skogai`, and the contracts are cut from that repo's `.skogai/scripts/claude/cloud-environment.sh`.
- `groups.csv` names `dash-skogai`, `skogai-routing`, `okn`, `config`, `dot-skogai`, `skogai`, `skogix`, `claude` as fleet members.
- The monorepo's mani catalog covers the same job as `repo list|add` (catalog and fetch); the files here do not mention mani.

## Gaps and stale references

- `SKOGAI.md` header says generated 2026-08-22 at commit `4166a81`; it describes `repo::workon` and `_repo_review_pr`, which are not in `Argcfile.sh`.
- `tests/argc-smoke.sh:35-36` checks `repo workon --help`, a command that does not exist at HEAD.
- `README.md:8` and `SKOGAI.md:78` show `repo list --type active`; no `--type` option is declared.
- `queue` commands reference missing `scripts/queue.sb` and `scripts/queue.sh`; `_choice_queue_args` has a syntax-suspect `args[-]=` (`Argcfile.sh:218`).
- `docs/dependencies.md:24` says `.envrc` adds `tmp/bin` and `bin` to `PATH`; `.envrc:6` adds `scripts/argc`.
- `.gitignore` contains a bare `/tmp` and `tmp/` while `tmp/**/.gitkeep` files are tracked.
- `todo.list` open items: undeclared `gitingest` dependency for `repo digest`, uncommitted `script_dir` fix (ADR 0002), bugs in `skogai module new|check`, six `skogai-networking` worktrees awaiting agents.
- `HANDOVER.md:147-151` open questions: where dispatch lives (core or runner) and whether cloud agents are a backend from the start. The move to skogai2 is answered by the origin URL.
- The `skogai-argc` skill exists three times (`.claude/skills/`, `.agents/skills/`, `docs/argc/`).
