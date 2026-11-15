---
type: repository
title: skogai2-skogai
description: The orchestration repo where skogix and agents plan and delegate - herdr work orders, the dash-skogai type system draft, local rules and memory, and a vv-harness setup. Active in early November 2026; most parts are specifications, not running code.
tags: [orchestration, herdr, work-orders, types, memory, harness]
repo: skogai2/skogai
commit: d836c2e
last_commit: 2026-11-10
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-skogai/AGENTS.md
  - repos/skogai2-skogai/SKOGAI.md
  - repos/skogai2-skogai/docs/skogix/introduction.md
  - repos/skogai2-skogai/mise.toml
  - repos/skogai2-skogai/hk.pkl
  - repos/skogai2-skogai/.gitignore
  - repos/skogai2-skogai/config/config.json
  - repos/skogai2-skogai/orchestration/README.md
  - repos/skogai2-skogai/orchestration/AGENTS.md
  - repos/skogai2-skogai/orchestration/work-orders/SPECIFICATION.md
  - repos/skogai2-skogai/orchestration/work-orders/completed/skogai-layout.md
  - repos/skogai2-skogai/dash-skogai/SKOGAI.md
  - repos/skogai2-skogai/dash-skogai/Argcfile.sh
  - repos/skogai2-skogai/dash-skogai/config
  - repos/skogai2-skogai/dash-skogai/mise.config.toml
  - repos/skogai2-skogai/dash-skogai/README.md
  - repos/skogai2-skogai/dash-skogai/type/index.md
  - repos/skogai2-skogai/dash-skogai/workflows/skogai.md
  - repos/skogai2-skogai/dash-skogai/tmp/definitions.md
  - repos/skogai2-skogai/.skogai/README.md
  - repos/skogai2-skogai/.skogai/memory/MEMORY.md
  - repos/skogai2-skogai/.skogai/journal.md
  - repos/skogai2-skogai/.skogai/scripts/claude/cloud-environment.sh
  - repos/skogai2-skogai/.claude/settings.json
  - repos/skogai2-skogai/.harness/harness.json
  - repos/skogai2-skogai/.harness/context_summary.md
  - repos/skogai2-skogai/.harness/features.json
  - repos/skogai2-skogai/.trail/README.md
---

# skogai2-skogai

**The orchestration repository: the place where the owner and a lead agent plan work, write work orders, and hand them to worker agents in isolated worktrees through the `herdr` CLI.** It also carries a draft type system for `.skogai/` folders (`dash-skogai/`), the local rules and memory agents read, and a vv-harness configuration. State: active, then paused. All 66 commits in the clone fall between 2026-11-01 and 2026-11-10, many of them automatic "journal and log" commits; the last three scaffold the `.skogai/` layout through the first completed work order. Stack per `AGENTS.md:7`: bash, mise, jq/yq, argc. There is little executable code; most content is specification and agent guidance.

## Source map

| Path | Holds |
|---|---|
| `AGENTS.md` | Agent entry point: commands, layout, harness, git identity, Trail instructions. `CLAUDE.md` is `@AGENTS.md`. |
| `SKOGAI.md` | One route, to `docs/skogix/introduction.md`. |
| `docs/skogix/introduction.md` | Short overview of layout, herdr workflow, Trail, tests. |
| `orchestration/` | Herdr hub: `README.md` (CLI reference and workflow), `AGENTS.md` (orchestrator rules), `work-orders/` (`SPECIFICATION.md`, `TEMPLATE.md`, `open/`, `completed/`). |
| `dash-skogai/` | Type system draft: `type/*.md` (13 types, 13 hook-event schemas, 6 tool pages), `workflows/skogai.md`, `Argcfile.sh`, `config` layers, generated `README.md`, `src/` (future dot), `tmp/` (vendored argc docs, routing copy, graph script, `definitions.md`). |
| `.skogai/` | `rules/` (13), `memory/` (25 entries, index `MEMORY.md`), `scripts/` (7), `templates/`, `tasks/`, `journal.md`, and ignored `state/`, `tmp/`, `worktrees/`. Layout documented in `.skogai/README.md`. |
| `.harness/` | vv-harness state: `harness.json`, `features.json` (F001-F003, all passing), `context_summary.md`, `init.sh`, `mld/` session notes. |
| `.claude/` | `settings.json` (permissions, hooks, marketplace), `hooks/` (vv-harness gates and statusline), `skills` symlink. |
| `.trail/` | Trail context-graph setup: `hook.cjs`, `workspace.json`, six `learnings/`. |
| `config/config.json` | An older skogcli-style config tree (agent namespaces, settings). |
| `mise.toml`, `hk.pkl` | Tools and two `dash:*` tasks; lint config. |
| `.codex/`, `.gemini/`, `opencode.json`, `GEMINI.md` | Per-agent config: rtk hook for Codex, Trail MCP for Gemini and opencode. |

## How it works

### Orchestration and work orders

`orchestration/AGENTS.md:9-15` sets the rule: a session in this directory is an orchestrator. It plans, delegates, supervises and verifies, and does not implement. The workflow in `orchestration/README.md` (steps 1-6) is:

1. Pick a work order from `work-orders/open/` and check its `owns` list does not overlap another open order.
2. `herdr worktree create --branch wo/<name> --no-focus` for an isolated worktree and workspace.
3. `herdr agent start worker-<name> --kind claude|codex` in that pane, in auto mode.
4. `herdr agent prompt ... --wait` with a brief that points at the work order file.
5. Poll with `herdr agent get|wait|read`; a `blocked` worker triggers an operator notification, never an automatic answer.
6. Verify from `git diff` in the worktree that changed files are a subset of `owns`, run the acceptance checks, then remove the worktree and move the order to `completed/`.

The README states it targets herdr v0.9.5, protocol 22, and forbids wrapper scripts around `herdr`.

A work order (`work-orders/SPECIFICATION.md:18-32`) is a Markdown file with YAML frontmatter: mandatory `name`, `description`, `reads` (context files) and `owns` (the exclusive write set, files only, no globs); optional `status`, `depends_on`, `tags`. Runtime targets such as `workspace`, `pane`, `worktree`, `agent`, `model`, `branch` are forbidden fields (`SPECIFICATION.md:49-67`). One order exists: `completed/skogai-layout.md`, which produced `.skogai/README.md` and the placeholder files. `open/` is empty.

### dash-skogai (type system draft)

`dash-skogai/SKOGAI.md:17-25` gives the design goals: a "dot" (a `.skogai/` folder) is a closed union of typed files; the OKF `type` frontmatter key is the tag; "dash" defines the cases; configuration resolves as a fold over layers; only `apply` writes.

- `type/<name>.md` defines a type with `fields`, `owns`, `writes`, `watches`. `tmp/definitions.md:15-29` tracks status: `tool` is defined; `type`, `decision`, `rule`, `trigger`, `event` are partial; `router` is draft; `knowledge`, `memory`, `task`, `spec`, `repo` are stubs.
- `type/event/*.schema.json` are JSON schemas for 13 Claude Code hook events.
- `workflows/skogai.md` is the `check` procedure written for an agent to follow by hand, because no CLI command exists. `plan` and `apply` are "not written yet" (`workflows/skogai.md:43-49`).
- `Argcfile.sh` has helper functions and no commands (`Argcfile.sh:3-5`); it would run `bin/skogai-<fn>`, and `bin/` does not exist.
- `config` is a git-config-style base layer; a key `a.b-c` maps to env `SKOGAI_A_BC` (`dash-skogai/config:1-2`). `mise.config.toml` sets `SKOGAI_CONFIG_SYSTEM_DIR`, `SKOGAI_CONFIG_LOCAL_DIR`, `SKOGAI_CONFIG_GLOBAL_DIR`.
- `README.md` is generated from `type/*.md` by `tmp/graph/types.sh` (one Mermaid graph per type).
- `tmp/routing/` is a copy of the skogai-routing skill (spec, schemas, validation scripts). I did not read its contents beyond the file list.

### Rules, memory, journal

`.skogai/rules/` holds standing agent rules (for example `herdr-orchestration.md`, `runner-conventions.md`, `scratch-in-repo-tmp.md`). `.skogai/memory/MEMORY.md` indexes 25 short notes, each with a `stale_after`. `.skogai/journal.md` (572 lines, tracked) is an automatic per-turn log of user prompts, assistant summaries and Bash commands written by the `skogai-core` plugin; the commit subjects "skogai-core: journal and log" come from it. I read the index and a sample, not every rule or memory file.

### Harness, hooks, Trail

`.claude/settings.json` wires PreToolUse hooks from `.claude/hooks/` (`enforce-scope.sh`, `verify-git-identity.sh`, `commit-gate.sh`), a `TaskCompleted` gate (`verify-task-quality.sh`), a statusline, `atuin hook claude-code` on Bash calls, the herdr session hook, and the Trail session-start hook. It registers `skogai-marketplace` from `skogai2/marketplace`. `hk.pkl:22` excludes `.claude/hooks/**` from lint because those files must stay identical to the vv-harness stamp. `.harness/context_summary.md` records harness decisions and herdr gotchas. `.trail/` connects the repo to a hosted Trail workspace; `AGENTS.md:36-70` tells agents to query it before reading source.

### Cloud setup script

`.skogai/scripts/claude/cloud-environment.sh` (166 lines) prepares a cloud container with many checkouts under `/workspace` and writes `/workspace/.cloud-setup/env.sh`. Its long comment header lists per-repo verified checks and known failures. `skogai2-core` treats that header as the source for per-repo contracts.

## How to use it

As defined in the files (not run):

- `mise install` for the tools in `mise.toml` (`age`, `argc`, `yq`, `jq`, `fnox`, `watchexec`, `shellcheck`, `shfmt`).
- `mise run dash:check [dot]`: runs `claude -p` read-only with an allowlist to perform the `check` workflow (`mise.toml:11-20`). Needs the `claude` and `okn` CLIs.
- `mise run dash:graph`: regenerates `dash-skogai/README.md`.
- `hk check --all` / `hk fix --all`: shellcheck, shfmt `-i 2 -ci`, private-key and merge-conflict detection.
- `.harness/init.sh smoke_test` / `full_test`.
- Orchestration needs `herdr`, `wt`, `yq`, `jq` and a running herdr session (`HERDR_WORKSPACE_ID`).
- Machine assumptions: `orchestration/` docs and the work order spec name `/home/skogix/skogai`; `settings.json` calls a hook at `/home/skogix/.claude/hooks/herdr-agent-state.sh`; `.harness/harness.json` pins a git identity that `verify-git-identity.sh` enforces.

## Relations to other SkogAI repos

- `skogai2-marketplace`: registered as `skogai-marketplace`; the source of the `skogai-core` and `vv-harness` plugins. `context_summary.md` names `skogai2/skogharness` as the origin of `/vv-harness:harness-orchestrate`.
- `skogai2-skogai-runner`: `workflows/skogai.md:26,45` defers open questions to `~/skogai-runner/TODO.md`; rules and memory (`runner-conventions.md`, `skogai-runner-is-a-command-runner.md`, `runner-and-mise-boundaries.md`) define its role as a command runner.
- `skogai2-skogai-routing`: copied into `dash-skogai/tmp/routing/`.
- `skogai2-dash-skogai`: shares the name of the `dash-skogai/` directory here but not its content; that repo is the `/skogai` workspace, this directory is a type-system draft.
- `skogai2-core`: its `HANDOVER.md` was written from a session here and builds its draft contracts from `cloud-environment.sh`. Core's workorder design (`.skogai/workorders/<id>.md`, `to:` field) differs from the `orchestration/work-orders/` format here.
- `skogai2-skogix`: its `.skogai/decisions/` cite this repo's `.skogai/workorders` and `bin/wo`; neither exists at this HEAD.
- `skogai2-skogai-fleet`: referenced by memory entry `fleet-persona-not-roleplay`.
- `config/config.json` sets `SKOGAI_CONFIG_DIR` per namespace (`dash-skogai`, `dot-skogai`, `skogai`, `harness`) and `SKOGAI_AGENT_NAME` per agent.

## Gaps and stale references

- `.claude/skills` is a symlink to `../.skogai/skills`, which is not in the tree.
- `AGENTS.md:12` mentions `bats -r tests/unit`; there is no `tests/` directory. `context_summary.md` confirms no tests exist yet.
- `dash-skogai/SKOGAI.md:8,11` mentions `TODO.md` and `bin/`; both are absent. `tmp/definitions.md:18` links `type/config.md`, which is absent, and notes decision `0006` is cited while no `type/decision/` exists.
- `MEMORY.md:3` cites "decision 0007"; the decision records are in `skogai2-skogix`, not here.
- `SKOGAI.md` routes only to the introduction and marks nothing else; `dash-skogai/SKOGAI.md:3-4` tags both its routes `[@TODO]`.
- `.gitignore` repeats the same log path four times; `.skogai/journal.md` is tracked and grows with every session.
- `.harness/context_summary.md` lists open gaps: the plan-rejection path and Claude plan-mode status were never observed live.
- `config/config.json` contains absolute paths under `/home/skogix` and looks like a carried-over file; nothing in the repo reads it.
- The Trail block in `AGENTS.md` refers to `.trail/cache/`, which is not tracked (local only).
