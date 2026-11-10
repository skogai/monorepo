# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`skogai/monorepo` is at a very early, pre-scaffolding stage. There is no build system, no tests, no language toolchain, and no lockfile yet. The language and tooling have not been decided. Do not invent build, lint, or test commands. Ask the user, or add the tooling yourself only when asked.

Current contents:
- `bin/claude`: a wrapper that sources `~/.ssh/SKOGAI_CLAUDE_CODE_OAUTH_TOKEN.env`, sets `CLAUDE_CONFIG_DIR=/home/skogix/.claude`, and then runs `exec claude "$@"`. Keep the `exec`: herdr identifies an agent by the pane's foreground process, and without it that process is `bash`.
- `mise.toml`: sets the same `CLAUDE_CONFIG_DIR` env var through mise. The path is hardcoded in both places, so a change to one must be made in the other too. The `CLAUDE_CODE_OAUTH_TOKEN` export in `bin/claude` is currently commented out (uncommitted), so the wrapper sources the env file but doesn't re-export the token under that name.
- `.skogai/research/`: research notes from Claude and Codex on monorepo direction (see below).
- `SKOGIX.md`: the user's notes. `TODO.md`: the open task list. The current item is adding fnox-based key handling and basic encryption through mise dotfiles/bootstrap.

## Secrets

- `SECRETSINHERE/` is gitignored and may contain live secrets. Never read, print, or commit anything from it.
- Treat any untracked file with restrictive permissions in the repo root (for example `quiz.aldervall.se`, mode 600) as potentially sensitive. Don't read or commit it without asking first.
- Credentials are loaded from files outside the repo (`~/.ssh/*.env`). Never inline their values.

## Direction under consideration

`.skogai/research/` holds two research write-ups. Read them before proposing structure. Neither is a decision. The recurring recommendations are:
- GitHub Issues and PRs for tickets. Markdown in Git (`docs/`) for durable knowledge. ADRs for decisions.
- `git grep` / `rg` as the baseline search. Any RAG layer (for example Postgres FTS + pgvector, or qmd) is rebuildable from Git and cites source files.
- Toolchain depends on the main language, which is still undecided. If Python-first: `pyproject.toml` + `uv.lock`, adding uv workspaces later. If JS: pnpm + Turborepo. If polyglot: Nx or Moon.
- mise is already used for env and tool management.

## Workflow notes

- Development happens in git worktrees (for example `claude-skogix-worktree`). The main branch is `master`.
