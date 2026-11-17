---
type: repository
title: skogai2-skogix
description: The owner's personal configuration repo, checked out at /skogai on his machine - clean-environment launchers and isolated config dirs for Claude Code, Antigravity and Codex, a docs-lookup plugin marketplace, decision records and personal notes. Work in progress.
tags: [personal-config, launchers, claude-code, plugins, decisions, wip]
repo: skogai2/skogix
commit: 6bce7e7
last_commit: 2026-11-09
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-skogix/CLAUDE.md
  - repos/skogai2-skogix/mise.toml
  - repos/skogai2-skogix/mise.md
  - repos/skogai2-skogix/hk.pkl
  - repos/skogai2-skogix/.gitmodules
  - repos/skogai2-skogix/.gitignore
  - repos/skogai2-skogix/bin/claude
  - repos/skogai2-skogix/bin/agy
  - repos/skogai2-skogix/claude/settings.json
  - repos/skogai2-skogix/claude/.gitignore
  - repos/skogai2-skogix/claude/shell/.zshrc
  - repos/skogai2-skogix/agy/settings.json
  - repos/skogai2-skogix/codex/run
  - repos/skogai2-skogix/codex/README.md
  - repos/skogai2-skogix/codex/AGENTS.md
  - repos/skogai2-skogix/codex/config.toml
  - repos/skogai2-skogix/.claude-plugin/marketplace.json
  - repos/skogai2-skogix/.agents/plugins.json
  - repos/skogai2-skogix/.codex/hooks.json
  - repos/skogai2-skogix/plugins/skogdocs/HANDOVER.md
  - repos/skogai2-skogix/.skogai/decisions/0003-repo-roles.md
  - repos/skogai2-skogix/.skogai/decisions/0005-dash-and-dot-skogai.md
  - repos/skogai2-skogix/.skogai/TODO.md
  - repos/skogai2-skogix/skogix/README.md
---

# skogai2-skogix

**The owner's personal configuration repository: launchers that start coding agents in a stripped environment, one isolated config directory per agent, a small plugin marketplace, and a `.skogai/` folder of decisions, notes and submodules.** `CLAUDE.md:7` says it is checked out at `/skogai` on the owner's machine and that almost every absolute path assumes that location, so the launchers and settings do not work from another path. There is no application to build. State: work in progress. The clone's 66 commits run from 2026-10-29 to 2026-11-09 with frequent "WIP" commits; the latest is "WIP".

## Source map

| Path | Holds |
|---|---|
| `CLAUDE.md` | The only root guide: layout, commands, conventions. Mostly accurate (see Gaps). |
| `mise.toml` | Entry point: env vars, `claude`/`agy` wrappers, lint tools. |
| `mise.md` | Reference notes on `mise bootstrap`, dotfiles and daemons. Not configuration. |
| `bin/claude`, `bin/agy` | Clean-environment launchers. |
| `claude/` | Project-scoped `CLAUDE_CONFIG_DIR`. Tracked: `settings.json`, `shell/.zshrc`. Everything else ignored by a deny-all `.gitignore`. |
| `agy/` | Same pattern for Google Antigravity: `settings.json`, `shell/.bashrc`, `shell/.zshrc`. |
| `codex/` | Codex CLI baseline: `run`, `config.toml`, `AGENTS.md`, `README.md`, `workspace/`. |
| `.claude-plugin/marketplace.json` | Makes the repo root a marketplace named `skogix` with one plugin. |
| `.agents/plugins.json` | Registers the `agy-docs-lookup` plugin for Antigravity. |
| `plugins/skogdocs/` | Standalone marketplace `code-docs-tools`: plugins `code-docs-lookup` and `agy-docs-lookup`, `tests/`, `tools/`, `HANDOVER.md`. |
| `scripts/claude/hooks/herdr-agent-state.sh` | Herdr-managed session hook. |
| `.skogai/decisions/` | Seven numbered decision records in OKF format (0001-0007, all `status: stable`). |
| `.skogai/personal/` | The owner's own docs and stories (34 files). |
| `.skogai/docs/cheat-sheets/` | 42 command cheat sheets. |
| `.skogai/repos/` | Seven git submodules. |
| `.skogai/TODO.md`, `.skogai/journal.md`, `.skogai/config/script_metadata.json` | Backlog, automatic session journal, generated metadata. |
| `skogix/` | A Python "autonomous coding agent demo" using the Claude Agent SDK. |
| `hk.pkl`, `.codex/hooks.json` | Lint config; `rtk hook codex` PreToolUse hook. |

## How it works

### Launchers and isolated agent configs

`mise.toml:8-12` defines wrappers so `claude` and `agy` resolve to `/skogai/bin/claude` and `/skogai/bin/agy`, and sets `CLAUDE_CONFIG_DIR=/skogai/claude` and `SKOGAI_CONFIG_DIR=/skogai/config`.

`bin/claude` runs `exec env -i` with an allowlist: `HOME`, `USER`, terminal and display variables, `SSH_AUTH_SOCK`, `PATH=/usr/local/bin:/usr/bin`, zsh as shell with `ZDOTDIR=/skogai/claude/shell`, and `CLAUDE_CONFIG_DIR`, then starts `$HOME/.local/bin/claude` (`bin/claude:2-18`). The agent's shell environment then comes only from `claude/shell/.zshrc`, which sets `PATH` and activates mise shims.

`bin/agy` does the same for Antigravity: it searches several mise install paths for the binary (`bin/agy:2-13`), adds `--settings /skogai/agy/settings.json` unless the caller passed one, and additionally passes through the `HERDR_*` variables and `COLLIE_INSTANCE` (`bin/agy:46-52`).

`codex/run` is different by design: it keeps the caller's environment and `HOME`, sets `CODEX_HOME`, `CODEX_SQLITE_HOME` and `TMPDIR` to subfolders of `codex/`, and starts `codex --no-daemon` from `codex/workspace/` (`codex/run:8-19`). `codex/README.md:37-43` states this is configuration separation, not a sandbox; `config.toml` sets `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.

Each config directory uses a deny-all `.gitignore` with `!` exceptions, so credentials, sessions and caches stay untracked (`claude/.gitignore`).

### Claude settings

`claude/settings.json` enables `skogai-core@skogai-marketplace`, sets `permissions.defaultMode` to `auto`, disables claude.ai MCP servers and policy skills through env flags, and registers three extra marketplaces: `vv-harness-marketplace` (GitHub `skogai2/skogharness`), `skogai-council-marketplace` and `bitwize-music` (directories under `/home/skogix`). It defines hooks for `SessionStart`, `SessionEnd`, `Stop`, `UserPromptSubmit` and `Notification`; the session hook path is `/skogai/claude/hooks/herdr-agent-state.sh`. I read the keys and marketplace entries, not every hook command.

### Plugins (`plugins/skogdocs/`)

Two plugins answer questions from a local copy of official docs instead of model memory. Per `HANDOVER.md`:

- `scripts/sync-docs.sh` downloads the docs bundle and splits it into one file per page plus an index.
- `scripts/search-docs.sh` finds pages containing all given terms; `show-doc.sh` prints a page or its headings and ends with a `source:` URL.
- `tools/build-env-reference.py` generates `references/env-vars.md` for the Claude plugin; `tools/build-cli-reference.py` exists for the agy plugin.
- `tests/run-case.sh` runs Claude with its own `CLAUDE_CONFIG_DIR` and an empty working directory; `tests/check-run.py` judges a run from its tool-call events.

The root marketplace lists `code-docs-lookup` by relative path (`.claude-plugin/marketplace.json:9-11`). I did not read the scripts themselves.

### `.skogai/` knowledge area

`decisions/` records choices made in October 2026: adopt OKF (0001), workorders dispatched to herdr agents in `wt` worktrees (0002), repo roles and gita tracking (0003), knowledge lifecycle (0004), dash- and dot-skogai layers with origin as the only source of truth (0005), push on land (0006), knowledge versus memory (0007). `CLAUDE.md:22` notes that several describe tooling in `skogai2/skogai`, not here.

`repos/` pins seven submodules from the `skogai2` org: `aube`, `demand`, `usage`, `hk`, `pitchfork`, `skogai-runner`, `skogai-routing`. They are not initialised by default. Many November commits are `repos: bump skogai-runner`.

### `skogix/` demo

A two-agent harness (initializer, then coding agent) built on `claude_code_sdk`: `autonomous_agent_demo.py`, `agent.py`, `client.py`, `security.py` (bash allowlist), `prompts/`. `CLAUDE.md` does not mention this directory. I read its README and file list only.

## How to use it

From the files (not run):

- Clone at `/skogai`; `mise.toml:3` stores the clone command as `SKOG_REPO_CLONE`.
- `mise install` for `hk`, `shellcheck`, `shellharden`, `shfmt`; then `claude` and `agy` go through the wrappers.
- `hk check --all` / `hk fix --all` lint shell scripts. Do not run `hk fix` inside submodules (`CLAUDE.md:24`).
- `/skogai/codex/run login`, then `/skogai/codex/run [-C /skogai]`.
- `git submodule update --init` to populate `.skogai/repos/`.
- skogdocs tests, from `plugins/skogdocs/`: `tests/offline.sh`, `tests/offline-agy.sh`, `tests/environment.sh`, `tests/run-all.sh`, and `tests/agent.sh` (a real `claude -p` run that calls the API). `CLAUDE.md:39` says to prepend `~/.local/bin` to `PATH` first.
- Prerequisites: `claude` at `$HOME/.local/bin/claude`, zsh at `/usr/bin/zsh`, `mise`, optionally `agy`, `codex`, `rtk`, herdr. The `skogix/` demo needs `ANTHROPIC_API_KEY`.
- Environment variables set by the repo: `CLAUDE_CONFIG_DIR`, `SKOGAI_CONFIG_DIR`, `SKOGAI_CLAUDE_CODE_DOCS_DIR`, `SKOG_REPO_CLONE`, `SKOG_WIP`.

## Relations to other SkogAI repos

- `skogai2-dash-skogai` also claims `/skogai`. Decision 0005 here says `/skogai` is dash-skogai, the shared layer, and `~/.skogai` is dot-skogai, the user layer; decision 0003 lists `~/skogix` as this repo's home. `CLAUDE.md` and every launcher put this repo at `/skogai` instead.
- `skogai2-skogai-runner` and `skogai2-skogai-routing` are submodules under `.skogai/repos/`.
- `skogai2-marketplace`: source of the enabled `skogai-core` plugin; `CLAUDE.md:18` says `vv-harness` comes through it from `skogai2/skogharness`.
- `skogai2-skogai`: decisions 0002-0006 describe its workorder tooling; decision 0003 names it the orchestrator and names this repo "skogix's own dump repo ... not a workorder target".
- `skogai2-skogai-fleet`: decision 0003 marks it parked.
- `scripts/claude/hooks/herdr-agent-state.sh` duplicates the hook in `skogai2-dash-skogai`.
- `.codex/hooks.json` and `hk.pkl` follow the same pattern as `skogai2-skogai`.

## Gaps and stale references

- `CLAUDE.md:18` says `claude/settings.json` registers the repo as a directory marketplace at `/skogai`; no such entry is in `extraKnownMarketplaces`. `skogai-marketplace` is enabled there but also not declared in that file.
- `CLAUDE.md:20` notes the herdr hook is tracked at `scripts/claude/hooks/` while settings call `/skogai/claude/hooks/herdr-agent-state.sh`, a path the deny-all `claude/.gitignore` keeps untracked.
- Commit `8fb3115` dropped the skogharness submodule, yet `vv-harness-marketplace` is still registered (plugin disabled).
- `mise.toml` sets `SKOGAI_CONFIG_DIR=/skogai/config`; the repo has `.skogai/config/` but no `config/`. `SKOGAI_CLAUDE_CODE_DOCS_DIR=claude/docs` points at an untracked path.
- Decision 0003 links `../repos/index.md` and mentions `old-skills/`; neither exists here.
- `.gitignore` lists `.skogai/journal.md`, but the file is tracked.
- Compiled `__pycache__/*.pyc` files are committed under `skogix/` and `plugins/skogdocs/tests/`.
- `.skogai/personal/docs/` and `.skogai/personal/story/` contain many same-named files (possible duplicates; not compared).
- `plugins/skogdocs/HANDOVER.md` open problems: the env reference cannot be read in `-p` runs; `--system-prompt` is unverified.
- `.skogai/TODO.md` has ten open personal items, including a `skogai module build --shell fish` problem and "quick history and background of skogai3.0".
