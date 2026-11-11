# mise / jdx toolkit survey

Run: Claude (Opus 5.5, Claude Code), skogix-workstation, `/home/skogix/Work`, base `9b3920f`, 2026-11-11.
Sources: mise docs in `~/.local/src/mise/docs` at mise commit `2e56e35c4` (read, not run), and tool versions and provenance on this machine (run). Machine facts hold for skogix-workstation only.

## Roles

| Tool | Job | Link to mise (from docs) |
|---|---|---|
| mise | Tools, environment, tasks, bootstrap, dotfiles | — |
| usage | CLI argument, help and completion spec | Built into tasks: `#USAGE` lines in file tasks, `usage` in TOML tasks; values reach the script as `usage_*` variables (`tasks/file-tasks.md`) |
| hk | Git hooks, lint/fix runner | Installed as a tool; example wiring through `mise watch` in `hooks.md` |
| fnox | Secrets; chooses the provider (age, 1Password, cloud stores) | `[secrets.fnox]` + task `secrets = [...]`: given to that task only, redacted from output; experimental (`environments/secrets/fnox.md`). Also an input source for `[bootstrap.secrets]` |
| pitchfork | Supervises daemons with readiness checks | `[daemons]`, `mise daemons`, tasks with `daemons`; experimental, pitchfork ≥2.25, off in safe mode (`daemons.md`) |
| aube | npm package manager | Embedded in mise's `npm:` backend (`dev-tools/backends/npm.md`) |
| packslip | Release distribution and verification | `packslip:` backend |

## Plugin types (`plugins.md`)

- Tool and backend plugins install tools. Built-in backends (`github:`, `aqua:`, `npm:` and others) usually make them unnecessary.
- Environment plugins set environment variables and PATH, and install nothing. `skogai/mise-plugin` is one.
- Package-manager plugins manage another program's packages through `[bootstrap.packages]`. They are a candidate for marketplace management.
- asdf plugins are legacy.
- `[plugins]` pins by `#tag`, `#branch` or a full SHA. Abbreviated SHAs are rejected.

Other mise features relevant here: `mise bootstrap` (packages, files, services, repos, shell activation; applies only when run explicitly) and `[dotfiles]` with age encryption (`dotfiles/encryption.md`).

## Machine observations (run on skogix-workstation)

| Tool | Version | Source |
|---|---|---|
| mise | 2026.11.5 | three binaries: `~/.local/bin`, `~/.local/share/../bin`, `/usr/bin` (pacman `mise-bin`) |
| usage | 6.12.1 | pacman `usage` at `/usr/bin`, ahead of the mise install on PATH |
| fnox | 1.48.0 | pacman `fnox-bin` at `/usr/bin`, ahead of the mise install on PATH |
| hk | 2.12.0 | mise, `latest` |
| pitchfork | 2.32.4 | mise, `latest` |
| aube | 2.10.0 | mise, `latest` |
| packslip | 1.11.3 | mise, `latest` |

Commands: `<tool> --version`, `which -a`, `pacman -Qo`. Not run: no task, hook, secret, daemon or plugin experiment.
