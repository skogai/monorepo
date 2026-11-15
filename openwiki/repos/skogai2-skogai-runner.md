---
type: repository
title: skogai2-skogai-runner
description: Bash command-runner for "skogai 3.0", mid-remake. After a deliberate reset on 2026-11-07 the live source is one read-only log reader; the earlier argc module implementation is kept under best-argc-version/.
tags: [bash, command-runner, argc, usage, mise, workorders]
repo: skogai2/skogai-runner
commit: 15c5bd4
last_commit: 2026-11-09
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-skogai-runner/AGENTS.md
  - repos/skogai2-skogai-runner/mise.toml
  - repos/skogai2-skogai-runner/Containerfile
  - repos/skogai2-skogai-runner/src/core/log/usage.sh
  - repos/skogai2-skogai-runner/tests/log.bats
  - repos/skogai2-skogai-runner/tests/fixtures/log/run.jsonl
  - repos/skogai2-skogai-runner/docs/README.md
  - repos/skogai2-skogai-runner/docs/design.md
  - repos/skogai2-skogai-runner/docs/plan.md
  - repos/skogai2-skogai-runner/docs/history.md
  - repos/skogai2-skogai-runner/TODO.md
  - repos/skogai2-skogai-runner/.todo.md
  - repos/skogai2-skogai-runner/.skogai/TODO.md
  - repos/skogai2-skogai-runner/.skogai/workorders/WORKORDERS.md
  - repos/skogai2-skogai-runner/.harness/context_summary.md
  - repos/skogai2-skogai-runner/.harness/features.json
  - repos/skogai2-skogai-runner/.harness/harness.json
  - repos/skogai2-skogai-runner/.claude/settings.json
  - repos/skogai2-skogai-runner/packaging/arch/PKGBUILD
  - repos/skogai2-skogai-runner/packaging/arch/skogai-runner.install
  - repos/skogai2-skogai-runner/best-argc-version/HANDOVER.md
  - repos/skogai2-skogai-runner/best-argc-version/bin/skogai
  - repos/skogai2-skogai-runner/best-argc-version/.claude-plugin/plugin.json
  - repos/skogai2-skogai-runner/best-argc-version/hooks/hooks.json
  - repos/skogai2-skogai-runner/best-argc-version/scripts/main.sh
  - repos/skogai2-skogai-runner/best-argc-version/modules/core/argc.sh
  - repos/skogai2-skogai-runner/best-argc-version/modules/runner/argc.sh
---

# skogai2-skogai-runner

**skogai-runner is the Bash command runner intended to become the single entry point of "skogai 3.0": commands declared once, used the same way by humans and agents, built from small modules.** It is a work in progress in the middle of a ground-up remake. On 2026-11-07 the config, module-install, run, contract-checker and main entry scripts were deleted on purpose (commit `75beb96`; their last state is commit `2913d23`), leaving one live script, `src/core/log/usage.sh`, and its test. The earlier argc-based module implementation is kept as reference under `best-argc-version/`. 70 commits fall between 2026-11-06 and 2026-11-09; the last three are automatic "skogai-core: journal and log" commits.

## Source map

118 tracked files.

| Path | Holds |
|---|---|
| `AGENTS.md` | The working instructions and the most accurate status text. `CLAUDE.md` only imports it. |
| `src/core/log/usage.sh` | The only live source file: a read-only reader of the run event log (91 lines). |
| `tests/log.bats`, `tests/fixtures/log/run.jsonl` | The Bats suite for the reader and its 13-line fixture log. |
| `mise.toml` | Tools (`argc`, `usage`, `jq`, `yq`, `bats`, all `latest`) and three tasks: `image`, `test`, `test:container`. |
| `Containerfile` | Arch Linux image with a non-root `dev` user and the mise tools; the repo is mounted at `/repo` at run time. |
| `docs/` | `why.md`, `history.md`, `design.md`, `plan.md`, `markdown-plus.md`, `declarations.md`, `argc-guide.md`, and an index `README.md`. `docs/argc/` and `docs/argc-completions/` are copied upstream argc references of unrecorded revision (24 files). |
| `best-argc-version/` | The earlier module-based runner (50 files): `bin/skogai`, `modules/{core,runner,memory,type}`, `scripts/main.sh`, `docs/module.md`, `HANDOVER.md`, two skills, a Claude Code plugin manifest (version 0.9.1) and a SessionStart hook. Not run by `bats tests`. |
| `.skogai/workorders/` | `WORKORDERS.md` (the queue's routing file), `done/` with seven finished workorders, `open/` empty. |
| `.skogai/TODO.md`, `TODO.md`, `.todo.md` | Three backlogs: the foundation-first plan, open type/config/router design questions, and old implementation todos. |
| `.skogai/journal.md`, `.skogai/logs/skogai-core/log.jsonl` | Hook-written session journal (1,414 lines) and hook event log. Machine-generated; the log contains absolute paths from the author's machine. |
| `.skogai/research/mise.md` | Research notes on mise as config storage (274 lines). |
| `.harness/` | vv-harness bookkeeping: `features.json` (F001-F005), `context_summary.md`, `claude-progress.txt`, `init.sh`, `harness.json`. |
| `.claude/` | `settings.json` and five hook scripts (scope enforcement, git-identity check, commit gate, task-quality check, statusline) plus `harness_state.py`. About 4,500 lines. |
| `packaging/arch/` | `PKGBUILD` for `skogai-runner-git` and its `.install` script. |

## How it works

### The live piece: the log reader

`src/core/log/usage.sh` runs under `usage bash` (shebang, line 1) and declares its CLI in `#USAGE` comments (lines 2-20). It reads a JSONL event log and never writes.

- Log path: `--log <file>` or `SKOGAI_LOG`, else `$XDG_STATE_HOME/skogai/run.jsonl`, else `~/.local/state/skogai/run.jsonl` (`usage.sh:15`, `:34`).
- `runs` prints one compact JSON object per run in first-seen order: `{run, module, revision, started, ended, outcome, verdict, changed}`. A run with no `end` event is listed with `ended`, `outcome` and `verdict` null (`usage.sh:53-67`).
- `show <run>` prints that run's raw lines unchanged; the argument is a full run id or a unique prefix (`usage.sh:69-85`).
- Lines that are not a JSON object with a string `run` are skipped and counted on stderr; exit stays 0.
- Exit codes: 0 answered, 1 `jq` missing, 2 bad arguments, unknown or ambiguous run, or unreadable log.

The event shape is visible in `tests/fixtures/log/run.jsonl`: `ts`, `event` (`check`, `exec`, `apply`, `end`), `input`, `id`, `run`, `module`, `revision`, `outcome`. The writer that produced these events (`src/core/run/usage.sh`) was deleted in the reset.

### The direction

`AGENTS.md` and `docs/design.md` describe three pieces:

- **usage + mise** as the interface (decided 2026-11-06). Scripts declare a CLI in `#USAGE` comments; `effect=` metadata is meant for agents through `usage mcp`. argc was the earlier interface and is no longer extended. `docs/design.md` still names argc as the interface.
- **mise** for the environment, tools and tasks. Config storage is undecided pending `.skogai/research/mise.md`.
- **Markdown+**: a module starts as a Markdown file whose typed frontmatter declares `depends_on`, `reads`, `writes`, `owns`, `watches` and defaults.

`docs/plan.md` gives five steps: contracts, one hand-prepared workorder, JSONL evidence, packaging as a bundle, growth. `.harness/features.json` holds the specs of what was built and then removed: F001 relationship contract checker, F002 staged run in Podman with enforced writable scope, F003 module format as a mise TOML, F004 config over mise layers, F005 module install by copy into mise `conf.d`. All five have status `blocked`, recorded as superseded by the remake.

### Workorders

`.skogai/workorders/WORKORDERS.md` defines a hand-run queue. A workorder is a Markdown+ file with `name`, `owns` (the only paths the agent may change) and `reads`, and body sections Intent, Deliverable, Acceptance, Out of scope, Report back. A lead session hands each `open/` file to an agent, which works on branch `wo/<name>` and opens a draft PR; the lead reviews and moves the file to `done/`. The file states that nothing here enforces capabilities or records evidence yet.

### The kept earlier implementation: `best-argc-version/`

`best-argc-version/bin/skogai` (21 lines) sets `SKOGAI_MODULE_PATH` and `SKOGAI_BIN`, asks the core module for a module's command and environment, and `exec`s `argc --argc-run` on it; anything else goes to core. The modules:

- `modules/core/argc.sh` (756 lines): `config get|set|unset|list|env|files` across system, global, local and module layers, and `module ls|show|command|test|build|sandbox|check|env|add|diff|new`.
- `modules/runner/argc.sh` (325 lines): typed agent io. `send` (prompt, files, JSON schema to typed output), `improve` (agent edits, prints a patch unless `--apply`), `wo new|run|ls`, `journal` (read back and harvest session journals). Schemas in `modules/runner/schemas/`.
- `modules/memory/argc.sh`: entries under `.skogai/memory/` with `stale_after`; `ls`, `stale`, `new`, `index`.
- `modules/type/argc.sh`: validates instance frontmatter against module-offered JSON schemas.
- `scripts/main.sh`: an older registry runner (`register`, `remove`, `ls`, `sync`) that builds a main Argcfile from a template.

`HANDOVER.md` dates this work to 2026-10-18 through 2026-10-23 and states its verification claims must be rechecked. Environment variables used across this tree include `SKOGAI_MODULE_PATH`, `SKOGAI_MODULE_DIR`, `SKOGAI_CONFIG_DIR`, `SKOGAI_LOCAL_DIR`, `SKOGAI_SYSTEM_DIR`, `SKOGAI_BIN`, `SKOGAI_RUNNER_MODEL` and `SKOGAI_RUNNER_JOURNAL`. I read the entry script, command declarations and handover; I did not read the module bodies or their Bats suites line by line.

### Harness and hooks

The repo uses the "Long-Running Agent Harness (vv-harness plugin)". `.claude/settings.json` wires PreToolUse hooks (`enforce-scope.sh` twice, `verify-git-identity.sh`, `commit-gate.sh`) and a TaskCompleted hook (`verify-task-quality.sh`). Per `AGENTS.md` the commit gate denies staging and committing in one command and scans staged additions for secrets. I did not read the hook scripts.

## How to use it

As the repo defines it (read, not run):

- `mise install` installs the tools.
- `mise run test`: `bats tests` on the host. Depends on `image`, which builds `skogai-runner-dev` with Podman and exits 0 without building when Podman is absent.
- `mise run test:container`: the same suite in the Arch container, repo mounted read-only at `/repo`. Requires Podman.
- `bats tests/log.bats`, or `bats -f '<regex>' tests/log.bats`, for one file or matching tests.
- `.harness/init.sh smoke_test | focused_test <file> | full_test`: harness checks (`bash -n`, optional `shellcheck`).
- The reader: `src/core/log/usage.sh runs [--log <file>]` and `show <run>`. Needs `usage` and `jq` on `PATH`.

Assumptions: `AGENTS.md` warns the system `yq` may not be mikefarah's yq. Its session-start section calls `wt step diff` (the worktree tool `wt`) and writes to `.skogai/tmp/`. A fixed git identity is named in `AGENTS.md` and `.harness/harness.json` and is checked by a hook.

## Relations to other SkogAI repos

- **skogai-core (plugin).** The "skogai-core: journal and log" commits, `.skogai/journal.md` and `.skogai/logs/skogai-core/log.jsonl` come from that plugin's hooks. `docs/plan.md` says run events used "the skogai-core envelope".
- **marketplace.** `HANDOVER.md` says the module tests ran from the marketplace repo, which had its own local `.skogai/modules/marketplace` module, a workflow job and a pre-commit hook running them. `best-argc-version/` is a Claude Code plugin named `skogai-runner`; `.todo.md` mentions `skogai marketplace evals skogai-runner` and `plugins/skogai-core/CONFIG.md`.
- **dash-skogai.** `TODO.md` is largely dash design questions (types, `dash.ref`, `mise run dash:check`, `mise run dash:graph`, a router type, decision 0006). `.todo.md` says a generated completion file comes from "the gone dash-skogai CLI" and that `~/skogai/dash-skogai/bin/skogai` no longer exists.
- **skogai2-cli.** `TODO.md` ends with a `skogai-config` item (port get/set/list/env/unset from `git config -f` to mise TOML layers), the module that repo holds.
- **old-core.** `.todo.md` names `~/old/old-core/Argcfile.sh` (repo, queue, tools) as a source to port from.
- **skogai-routing.** `WORKORDERS.md` uses `type: routing` and a `permalink`, the routing-file convention.
- **okf / okn.** `TODO.md` refers to `okn validate`, `typed_links` and the OKF `status` and `stale_after` fields as the schema base for types.
- The same repo name in the older `skogai` org was "Repository not found" per the monorepo survey; this is skogai2 only.

## Gaps and stale references

- `AGENTS.md`, `docs/README.md`, `docs/design.md` and `docs/plan.md` point at `best-version-so-far/`. The directory was renamed `best-argc-version/` (commit `87b85e9`), so those links are broken.
- `packaging/arch/PKGBUILD:31` installs `src/core/main.sh`, which was deleted. `skogai-runner.install` tells the user to run `argc --argc-run /usr/share/skogai/core/main.sh sync`. `AGENTS.md` acknowledges this.
- `docs/README.md` links `../README.md` and `runner.md`; neither exists. `docs/evidence.md`, cited by `usage.sh:5` and `tests/log.bats`, does not exist.
- `docs/plan.md` "Current status" and `WORKORDERS.md` describe deleted files as implemented (`src/core/contract/`, `src/core/run/`, `main-usage.sh`, `examples/hello`, `tests/run.bats`, `tests/examples.bats`). The queue-check command in `WORKORDERS.md` calls the deleted `src/core/contract/usage.sh`.
- `.harness/context_summary.md` says the remake is on branch `remake/config`, "not merged"; whether the cloned default branch is that state merged was not checked beyond the log showing the reset commits in history.
- Config storage is undecided. No workorder is open.
- `.gitignore` lists `/.skogai/logs/skogai-core/log.jsonl` four times, yet the file is tracked.
- `AGENTS.md` and `.todo.md` repeat the same Session start, Harness and Git identity sections.
- `mise.toml` pins every tool to `latest`.
