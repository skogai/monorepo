# Repository Guidelines

## Project Structure & Module Organization

This repository tracks user-level systemd configuration for SkogAI services.
Top-level `*-start.sh` files are executable wrappers used by units in `user/`.
Service units live in `user/*.service`; timers live beside them, for example
`user/gptme-agent-dot.timer`. Enablement state is represented by symlinks under
`user/default.target.wants/` and `user/sockets.target.wants/`. Keep the service
inventory, ports, and operational notes in `README.md` synchronized with unit
changes.

## Build, Test, and Development Commands

There is no build step. Validate changes before applying them to the live user
systemd directory:

```bash
systemd-analyze verify user/skogai-codex-web.service
bash -n skogai-codex-web-start.sh
systemctl --user daemon-reload
systemctl --user restart skogai-codex-web
journalctl --user -u skogai-codex-web -n 50
```

Use `systemctl --user status skogai-*` for broad state checks. Use `journalctl
--user -u <unit> -f` when debugging restart loops or environment issues.

## Coding Style & Naming Conventions

Name SkogAI units `skogai-<service>.service` and matching wrappers
`skogai-<service>-start.sh`. Prefer `%h` in unit files for home-relative paths
unless an existing service intentionally uses an absolute path. Shell wrappers
should use Bash, start with `#!/usr/bin/env bash`, and prefer
`set -euo pipefail` for non-trivial scripts. Keep environment setup explicit:
set `PATH`, source NVM only when needed, and avoid embedding secrets in tracked
files.

## Testing Guidelines

For each changed unit, run `systemd-analyze verify` on the unit file. For each
changed wrapper, run `bash -n`. If behavior changes, restart only the affected
unit and confirm logs plus the relevant port or socket. Examples:
`curl -fsSI http://127.0.0.1:9994` for HTTP services, or `codex app-server
daemon version` for the Codex app-server daemon.

## Commit & Pull Request Guidelines

Recent history uses short, lowercase imperative commits such as `add
plan.skogai.se`. Keep commits focused on one service or related stack. PRs
should describe the affected units, why the service behavior changed, validation
commands run, and any README updates. Include log excerpts only when they explain
a failure or confirm a fix.

## Agent-Specific Instructions

Also follow `/home/skogix/skogai/AGENTS.md`: use the codebase wiki workflow when
making code changes in that project. In this repository, start from current files
and live service state before relying on prior memory.
