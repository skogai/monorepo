---
type: repository
title: skogai2-dash-skogai
description: The repo meant to be checked out at /skogai as the shared multi-agent workspace - admin scripts, gptme launcher generator, Claude Code hooks. Work in progress; the README describes several paths that have been deleted.
tags: [workspace, multi-agent, gptme, hooks, mise, wip]
repo: skogai2/dash-skogai
commit: 5388992
last_commit: 2026-11-01
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-dash-skogai/README.md
  - repos/skogai2-dash-skogai/SKOGAI.md
  - repos/skogai2-dash-skogai/.gitignore
  - repos/skogai2-dash-skogai/.gitmodules
  - repos/skogai2-dash-skogai/mise.toml
  - repos/skogai2-dash-skogai/fnox.toml
  - repos/skogai2-dash-skogai/admin/create-agents.sh
  - repos/skogai2-dash-skogai/admin/setup-coordination.sh
  - repos/skogai2-dash-skogai/admin/install-tools.sh
  - repos/skogai2-dash-skogai/admin/install-coordination.sh
  - repos/skogai2-dash-skogai/admin/test-coordination.sh
  - repos/skogai2-dash-skogai/scripts/gen-bin.py
  - repos/skogai2-dash-skogai/scripts/claude/hooks/herdr-agent-state.sh
  - repos/skogai2-dash-skogai/scripts/claude/hooks/rtk-suggest.sh
  - repos/skogai2-dash-skogai/scripts/claude/hooks/worktree-create.sh
  - repos/skogai2-dash-skogai/.skogai/logs/hook-tap/log.jsonl
---

# skogai2-dash-skogai

**The repository that is meant to be the `/skogai` directory: a shared, group-writable workspace where several Unix users (a human and agent accounts) use the same tools and one coordination database.** It holds the admin scripts that create that setup, a generator for `gptme` launchers, and a few Claude Code hook scripts. State: work in progress and small (16 tracked files). Activity ran from 2026-10-02 to 2026-10-18, mostly "WIP" commits, then one merge on 2026-11-01 that added `SKOGAI.md`. The 2026-10-09 and 2026-10-18 commits deleted the fish config, the config defaults, the knowledge bundle and the `gptme-contrib` submodule, but `README.md` and `SKOGAI.md` still describe them.

## Source map

| Path | Holds |
|---|---|
| `README.md` | Layout table, bootstrap steps, permissions, gotchas. Partly stale (see Gaps). |
| `SKOGAI.md` | Short agent entry point routing to `README.md`. Partly stale. |
| `admin/create-agents.sh` | Creates the `skogai` group and agent system users. Needs root. |
| `admin/setup-coordination.sh` | Sets ownership and modes on `/skogai` and `/skogai/coordination`, pre-creates `coord.db`. Needs root. |
| `admin/install-tools.sh` | Installs `uv` and `python` under `tools/mise` and runs `scripts/gen-bin.py`. |
| `admin/install-coordination.sh` | Older venv-based install of `gptme-coordination`; the README says `install-tools.sh` replaces it. |
| `admin/test-coordination.sh` | Cross-user smoke test of `gptme-coordination`. Needs root. |
| `scripts/gen-bin.py` | Generates `bin/` launchers for gptme and each gptme-contrib package. Holds the version pins. |
| `scripts/claude/hooks/` | `herdr-agent-state.sh` (herdr-managed), `rtk-suggest.sh`, `worktree-create.sh`. |
| `mise.toml` | Tools (`uv`, `python`, `openknowledge`), `bin/` on `PATH`, `SKOGAI_USER`, `SKOGAI_MODE`. |
| `fnox.toml` | fnox secret-provider config with three age providers and three example secrets. |
| `.skogai/logs/hook-tap/log.jsonl` | A committed 257-line hook event log from one session on 2026-10-09. |
| `.gitmodules` | Empty file. |
| `.gitignore` | Ignores `/bin/`, `/tools/`, `/coordination/`, `/tmp/`. |

Not tracked, created by the scripts: `bin/`, `tools/`, `coordination/`.

## How it works

### Users, group and permissions

`admin/create-agents.sh` creates a system group `skogai` and one system user per agent with home `/home/<name>` and a `nologin` shell. Defaults in the script are `claude dot amy goose codex` (`create-agents.sh:11`); the header comment and README list four. Humans named in `HUMANS` are added to the group if the user exists.

`admin/setup-coordination.sh` hard-codes `ROOT=/skogai` (`setup-coordination.sh:13`). It makes `/skogai` and `/skogai/coordination` owned by `skogix:skogai` with mode `2775` (setgid), and pre-creates `coordination/coord.db` as `0664`. The script comments explain why: SQLite creates databases as `0644` and gives `-wal`/`-shm` files the same mode as the main file, so the file must exist group-writable first (`setup-coordination.sh:36-39`).

`bin/` and `tools/` are set to `755`, not group-writable, because every user executes the launchers; a group-writable `bin/` would let one agent plant code that runs as another (`install-tools.sh:14-17`).

### Launchers (`scripts/gen-bin.py`)

`install-tools.sh` sets `MISE_DATA_DIR` to `<root>/tools/mise`, installs `uv` and `python` through mise, then runs `gen-bin.py` with that Python.

`gen-bin.py` writes one bash launcher per console script into `bin/`:

- gptme core scripts come from a fixed list (`gen-bin.py:34-41`) at `GPTME_SPEC` (`gen-bin.py:31`).
- gptme-contrib scripts are discovered by reading `gptme-contrib/packages/*/pyproject.toml` (`gen-bin.py:88-110`). Each installs from `CONTRIB_URL` at the commit in `CONTRIB_REF`, with `#subdirectory=packages/<pkg>`.
- Workspace-sibling dependencies are added as extra `--with` specs; packages depending on `mcp` get `mcp<2` (`gen-bin.py:94-107`).

Each launcher (template at `gen-bin.py:43-59`) resolves `uv` through mise, exports `COORDINATION_DB` defaulting to `<root>/coordination/coord.db`, and execs `uv tool run --from <spec> <cmd>`. The comment at `gen-bin.py:25-29` says installs use the full commit SHA because a tag is re-fetched on every call.

The discovery step reads the `gptme-contrib/` directory, which is no longer in the tree (see Gaps).

### Environment (`mise.toml`)

`mise.toml:13-15` derives two variables from the Claude Code environment: `SKOGAI_USER` is `claude` when `CLAUDECODE` is defined, otherwise `skogix`; `SKOGAI_MODE` is `remote` when `CLAUDE_CODE_REMOTE` is `true`, otherwise `workstation`. A commented block sketches per-user fnox profiles and example tasks. `fnox.toml` defines providers `shared-age`, `skogix-age`, `claude-age` and the example secrets `MY_SECRET_LOCAL_SKOGIX_ONLY`, `MY_SECRET_LOCAL_CLAUDE_ONLY`, `OUR_SHARED_LOCAL_SECRET` (encrypted values, committed).

### Claude Code hooks

- `herdr-agent-state.sh`: installed and managed by herdr (integration version 11). On `SessionStart` it reports the session id and transcript path to the herdr socket named by `HERDR_SOCKET_PATH` for pane `HERDR_PANE_ID`. It exits silently outside herdr.
- `rtk-suggest.sh`: a `PreToolUse:Bash` hook that prints a `systemMessage` suggesting the `rtk` equivalent of common commands (git, gh, cargo, cat, grep, ls, docker and others). It does not rewrite the command.
- `worktree-create.sh`: a `WorktreeCreate` hook that delegates to `wt switch --create <name> --no-cd --format json` and prints the resulting path, so Worktrunk pre-start hooks run before the session starts.

No settings file in this repo registers these hooks; they are sources to be referenced from a Claude Code config elsewhere.

## How to use it

From `README.md:23-29` (read, not run):

```bash
sudo bash admin/create-agents.sh [names...]
sudo bash admin/setup-coordination.sh
bash admin/install-tools.sh
sudo bash admin/test-coordination.sh
export PATH=/skogai/bin:$PATH
```

- Prerequisites: root for three of the scripts, `mise` on `PATH`, network access to GitHub for `uv tool run`.
- Machine assumptions: checkout at `/skogai`; a user named `skogix`; `test-coordination.sh` hard-codes `/skogai/bin/gptme-coordination` and `/skogai/coordination/coord.db`. `install-tools.sh` and the launchers resolve their own root and are written to work from any checkout path.
- The README says the first call of each launcher builds into the calling user's uv cache and recommends warming launchers used inside time-limited hooks.
- To bump gptme-contrib: change `CONTRIB_TAG` and `CONTRIB_REF` in `scripts/gen-bin.py` and rerun `install-tools.sh`.
- Environment variables by name: `COORDINATION_DB`, `SKOGAI_BIN`, `SKOGAI_USER`, `SKOGAI_MODE`, `MISE_DATA_DIR`, `FNOX_PROFILE` (commented).

## Relations to other SkogAI repos

- `dash-skogai` in the older `skogai` org has the same name and role; this clone's files do not reference it. Both assume the `/skogai` path.
- `skogai2-skogix` also assumes it is checked out at `/skogai`. The two cannot both be there.
- `skogai2/gptme-contrib` (fork): the launchers install from it; it was a submodule here until 2026-10-18.
- `skogai2-skogai-routing`: `README.md:4` points to `skogai-routing/references/dash-skogai.md` for the definition of this workspace.
- `skogai2-skogai` contains a `dash-skogai/` directory with different content (a type system and an argc CLI stub). It is not a copy of this repo.
- `herdr-agent-state.sh` is the same herdr-managed hook that appears in `skogai2-skogix/scripts/claude/hooks/`.
- The committed hook log shows a session run from a `skogai` worktree named `wo-0007-survey-dash-skogai` with this repo at `~/.local/src/dash-skogai`, matching the survey workorder that decision 0005 in `skogai2-skogix` cites.

## Gaps and stale references

- `README.md:11` lists `knowledge/` (OKF bundle); the bundle lived at `.skogai/knowledge/` and was deleted on 2026-10-18.
- `README.md:15`, `SKOGAI.md:17-20` describe a `gptme-contrib/` submodule; it was removed on 2026-10-18 and `.gitmodules` is empty. `install-tools.sh:11` still runs `git submodule update --init gptme-contrib`, and `gen-bin.py` needs that directory to find contrib packages.
- `README.md:19` lists `fish/`; `SKOGAI.md:23-25` describes `config.defaults.json` and `default/`. All were removed on 2026-10-09.
- `README.md:48-49` warms `gptme-cc-memory-*` launchers; the matching hook scripts were removed on 2026-10-10.
- `worktree-create.sh` refers to `.config/wt.toml`; this repo has none.
- `create-agents.sh` comment and README list four default agents; the code has five.
- `.skogai/logs/hook-tap/log.jsonl` is a committed log containing local paths and session content; `.gitignore` does not exclude it.
- No tests, CI or lint config are tracked.
