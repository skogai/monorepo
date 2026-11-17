---
type: repository
title: skogai2-config
description: The knowledge and health-check repo for the owner's workstation configuration ("skogai config 3.1"). Markdown pages grouped by concern plus bash checks; it holds no dotfiles or secrets itself. Active, last commit 2026-11-15.
tags: [machine-config, mise, dotfiles, health-checks, secrets, bash]
repo: skogai2/config
commit: d21d332
last_commit: 2026-11-15
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-config/README.md
  - repos/skogai2-config/AGENTS.md
  - repos/skogai2-config/SKOGAI.md
  - repos/skogai2-config/PROJECT.md
  - repos/skogai2-config/.skogai/TODO.md
  - repos/skogai2-config/.skogai/handover.md
  - repos/skogai2-config/.mcp.json
  - repos/skogai2-config/.codex/config.toml
  - repos/skogai2-config/bin/health
  - repos/skogai2-config/bin/health-lib.sh
  - repos/skogai2-config/bin/check-routes
  - repos/skogai2-config/bin/check-coverage
  - repos/skogai2-config/bin/test
  - repos/skogai2-config/mise/SKOGAI.md
  - repos/skogai2-config/mise/health
  - repos/skogai2-config/mise/bootstrap.md
  - repos/skogai2-config/mise/dotfiles.md
  - repos/skogai2-config/mise/adopt.md
  - repos/skogai2-config/mise/dotfiles-upstream.md
  - repos/skogai2-config/mise/secrets.md
  - repos/skogai2-config/mise/coverage.md
  - repos/skogai2-config/mise/coverage-triage.md
  - repos/skogai2-config/mise/old-dotfiles.md
  - repos/skogai2-config/secrets/fnox.md
  - repos/skogai2-config/secrets/health
  - repos/skogai2-config/shell/atuin.md
  - repos/skogai2-config/shell/bash.md
  - repos/skogai2-config/shell/zsh.md
  - repos/skogai2-config/shell/health
  - repos/skogai2-config/containers/podman.md
  - repos/skogai2-config/containers/health
  - repos/skogai2-config/desktop/window-manager.md
  - repos/skogai2-config/desktop/tmux.md
  - repos/skogai2-config/desktop/nvim.md
  - repos/skogai2-config/desktop/health
  - repos/skogai2-config/agents/herdr.md
  - repos/skogai2-config/agents/health
  - repos/skogai2-config/machine/SKOGAI.md
  - repos/skogai2-config/machine/health
  - repos/skogai2-config/machine/units/skogai-health.service
  - repos/skogai2-config/tests/lib.sh
---

# skogai2-config

**The entry point for how the owner's workstation is configured: one Markdown page per tool, grouped by concern, plus read-only bash health checks.** The repo holds no dotfiles and no machine state. Dotfiles stay in `~/.config` and are versioned by `mise dotfiles`; machine state is declared in the mise global config; secrets are planned for fnox with age (`README.md:7-18`). It is written for agents first. State: active. 50 commits in the shallow clone from 2026-10-31 to 2026-11-15, pages carry dated entries up to 2026-11-14, and the project plan (`PROJECT.md`, "config 3.1") has many open items. On the workstation the repo is checked out at `~/.config/skogai`.

## Source map

| Path | Holds |
|---|---|
| `AGENTS.md` | Routes, "where things are saved", how to work here, tool-shell gotchas |
| `SKOGAI.md` | The root router (a `<routes>` block), history of the config, tool list, environments |
| `README.md` | What the repo is and the three working rules |
| `PROJECT.md` | The 3.1 plan: principles, "done when", four work sections with checkboxes, planned modules and env vars |
| `.skogai/TODO.md`, `.skogai/handover.md` | Short to-do list; session handover (dated 2026-11-11) |
| `bin/health`, `bin/health-lib.sh` | The health runner and the helpers concern scripts source |
| `bin/check-routes`, `bin/check-coverage` | Route resolver check; `~/.config` coverage check |
| `bin/test` | Test runner: `smoke_test`, `focused_test <file>`, `full_test` |
| `tests/` | Eight `*.test.sh` files and `lib.sh`; everything runs against stubs and fixtures |
| `mise/` | The largest group: `bootstrap.md`, `dotfiles.md`, `adopt.md`, `dotfiles-upstream.md`, `secrets.md`, `coverage.md`, `coverage-triage.md`, `old-dotfiles.md`, `health` |
| `secrets/` | `fnox.md` (draft key and access model), `health` |
| `shell/` | `atuin.md`, `bash.md`, `zsh.md`, `health` |
| `containers/` | `podman.md` (Docker to rootless Podman), `health` |
| `desktop/` | `window-manager.md`, `tmux.md`, `nvim.md`, `mappings.md`, `health` |
| `agents/` | `herdr.md` (terminal workspaces for agents), `health` |
| `machine/` | `health` (failed user units) and `units/` (three systemd user units for the hourly check) |
| `.mcp.json`, `.codex/config.toml` | MCP servers `mise` and `atuin` for Claude Code and Codex |
| `.claude/settings.json` | Enables one Claude Code plugin |

Each concern directory has a `SKOGAI.md` router and an executable `health`.

## How it works

### Routers and routes

Navigation is by `<routes>` blocks. A route is the first word of a `- ` line inside `<routes>...</routes>`; a leading `@` is dropped and `[@TODO...]` placeholders are skipped. `bin/check-routes` finds every Markdown file with such a block and checks that each route exists, relative to the router's directory, or under `$HOME` for `~/` routes (`bin/check-routes:14-29`). Prose mentions are not routes (`AGENTS.md:26-27`).

### Health checks

`bin/health` runs every executable `<group>/health` one level below the root, plus `bin/check-routes` as group `skogai` (`bin/health:48-57`). The contract (`bin/health:1-13`): a concern script prints `ok <check>[: detail]` or `FAIL <check>: detail` lines, exits 0 only if it printed no `FAIL`, reads machine state only, and never prints env or secret values. The runner prefixes each line with the group, applies a timeout (`HEALTH_TIMEOUT`, default 120 s), turns a timeout, an empty report or an unexplained non-zero exit into a `FAIL health` line, and ends with `all N checks ok` or `F of N checks failed` (exit 0 or 1; 2 if the root is not a directory). A new concern joins by adding one file.

| Group | Checks | What they read |
|---|---|---|
| `skogai` | `routes` | `bin/check-routes` |
| `mise` | `doctor`, `bootstrap-plan`, `dot-capture`, `dot-sync`, `dot-modes`, `dot-links`, `coverage` | `mise doctor` (problem block only), `mise bootstrap plan`, `mise dot status`, `mise bootstrap status --json`, `mise dot paths --json`, `bin/check-coverage` (`mise/health:22-156`) |
| `secrets` | `ssh-dir`, `age-keys`, `fnox-config` | Modes and owners only, never contents (`secrets/health:12-58`) |
| `shell` | `atuin-sync` | `atuin status`, last sync within `ATUIN_SYNC_MAX_AGE_HOURS` (default 24) |
| `containers` | `quadlet-health` | Wraps the `quadlet-health` script from the quadlet repo |
| `desktop` | `tmux-config`, `hypr-bindings` | `stock_check`: fails when the personal file is missing or byte-identical to Omarchy's stock copy (`bin/health-lib.sh:38-52`) |
| `agents` | `herdr-config`, `herdr-binary`, `herdr-integrations` | Stock check, which `herdr` is first on `PATH`, `herdr integration status` |
| `machine` | `failed-units` | `systemctl --user --failed` |

That is 19 checks, the number the handover gives. The three units in `machine/units/` run `bin/health` hourly as a systemd user timer and send a critical desktop notification on failure; the service sets its own `PATH` with `~/.local/bin` first (`machine/units/skogai-health.service:9-10`, reason in `machine/SKOGAI.md:32-38`).

### Coverage

`bin/check-coverage` lists every entry directly in `~/.config` and sorts each as tracked (a `mode = "track"` entry in `mise dot paths --json`), decided (an `exclude` or `owner` row in the table in `mise/coverage.md`) or undecided. A name both tracked and decided is a `CONFLICT`. Exit 0 only with no undecided entries and no conflicts (`bin/check-coverage:50-79`). `mise/coverage.md` holds 67 decision rows with reasons; `PROJECT.md:109` records 65 tracked, 60 decided, 0 undecided on 2026-11-09.

### What the pages record

- **mise as the base** (`mise/SKOGAI.md`, `mise/bootstrap.md`, `mise/dotfiles.md`, `mise/adopt.md`): `~/.config` is tracked in place by path rules, never by symlink deploy. The history is published to a private origin, `skogai2/.dotfiles`. `[bootstrap.*]` in `~/.config/mise/config.toml` declares packages (divergences from Omarchy only), the `skogai` group, services, repos and fish activation. A fresh machine is meant to become this one with `mise bootstrap --adopt skogai2/.dotfiles`; `adopt.md` explains that flow from the mise source with `file:line` citations. The pages also keep rules learned from incidents, for example: never write a `[dotfiles]` entry without `mode = "track"` (`mise/dotfiles.md:69-76`).
- **Secrets** (`secrets/fnox.md`, `mise/secrets.md`): a draft model. Secrets go in fnox encrypted with age; separation between the owner and agent users comes from file permissions on identity files; the shared config is to live at `/etc/skogai/fnox.toml`, root-owned. Nothing real has been moved yet.
- **Shell** (`shell/`): fish is the login shell; atuin syncs history; atuin's dotfile vars became read-only legacy data in atuin 18.24, so env vars and aliases need a new home; bash and zsh were set up on 2026-11-14 with argc-completions and `usage`.
- **Containers** (`containers/podman.md`): Docker was replaced by rootless Podman on 2026-10-07; the running stacks are quadlets in their own repo.
- **Desktop** (`desktop/`): an i3-style keybinding scheme ported to Hyprland on Omarchy, tmux changes relative to Omarchy's defaults, and nvim as its own repo.
- **Agents** (`agents/herdr.md`): herdr setup, keybindings mirroring tmux, and conventions for agents that drive herdr panes.

### Tests

`tests/*.test.sh` source `tests/lib.sh` (`run`, `expect`, `refute`, `stub`, `toolbox`) and exercise the scripts against stub commands and temporary homes; `tests/health.test.sh:1-4` states that nothing reads live machine state.

## How to use it

Commands the repo defines (not run for this page):

- `bin/health`: all checks. Meant to run at session start (`AGENTS.md:32-33`). Overrides: `SKOGAI_HEALTH_ROOT`, `HEALTH_TIMEOUT`.
- `bin/check-coverage`: overrides `CONFIG_DIR`, `COVERAGE_FILE`. Needs `mise` and `jq`.
- `bin/check-routes [repo-root]`.
- `bin/test smoke_test | focused_test <file> | full_test` (default `full_test`: every test file, then `bin/check-routes`).
- Installing the timer by hand: `systemctl --user link` the three unit files, then `enable --now skogai-health.timer` (`machine/SKOGAI.md:25-30`).

Working rules (`README.md:20-28`, `mise/SKOGAI.md:26-39`): read a concern's page before changing anything in it; read-only commands run freely and anything that writes to the machine or pushes is confirmed first; never read secret values into a conversation (`mise env`, `fnox get`, env files); every `mise dot` write goes through one lead agent.

Machine assumptions:

- An Omarchy (Arch Linux, Hyprland) workstation with mise, atuin, herdr, podman, jq and systemd user units. The health scripts report `FAIL ... not found` where a tool is missing.
- The checkout path `~/.config/skogai` is hard-coded in the service unit (`%h/.config/skogai/bin/health`) and, as an absolute path in one user's home, in `.mcp.json` and `.codex/config.toml`.
- Override variables by name: `OMARCHY_CONFIG`, `HERDR_OMARCHY_BIN`, `QUADLET_HEALTH`, `FNOX_CONFIG`, `FNOX_CONFIG_OWNER`, `ATUIN_SYNC_MAX_AGE_HOURS`.
- Secret-bearing files the pages name (names only): age identity files under `~/.ssh/` matching `*age*.txt`, `/etc/skogai/fnox.toml` (ciphertext config), `~/.config/mise/ollama.secret.env` holding `SKOGAI_OLLAMA_API_KEY`, `/etc/cloudflared/token`, gptme's `server.env`, `~/.ssh/atuin.key.encrypted`, and `FNOX_AGE_KEY` for cloud sessions. None of their values are in the repo.

## Relations to other SkogAI repos

- **`skogai2/.dotfiles`** (private): the origin of the mise dotfile history that this repo documents. Its layout (`home/`, `config/`, `.mise-history/`, `.skogai/`) is described in `mise/dotfiles-upstream.md:18-25`.
- **`skogai/podman`**: the quadlet stack at `~/.config/containers/systemd`, its own repo; `containers/health` wraps its `bin/quadlet-health`, and `containers/SKOGAI.md` routes to its `SKOGAI.md`.
- **`skogai/nvim-omarchy`** (private): `~/.config/nvim`, its own repo since 2026-11-13 (`desktop/nvim.md:14-18`).
- **`skogai2/claude-home`**: the `claude` agent user's global mise config, adopted with `mise bootstrap remote` (`secrets/fnox.md:123-134`).
- **Bootstrap repos** declared on the workstation (`mise/bootstrap.md:22`): `~/.config/skogai` (this repo), `~/codex`, `~/.config/nvim`, `~/.config/containers/systemd`, `~/skogai`, `~/skogix`, `~/Work`. `~/Work` is the monorepo checkout according to [skogix](skogix.md). `~/.skogai` (dot-skogai) and `/skogai` (dash-skogai, whose origin is now `skogai2/skogix`) are commented out until set up again (`mise/bootstrap.md:158-160`).
- **dash-skogai**: `agents/herdr.md:20` loads fish completion from `dash-skogai/fish/config.fish`, and Claude's herdr hook links into `/skogai/scripts/claude/hooks/`.
- **skogai2-skogai-runner**: `~/.config/argc/commands/core.sh` is a symlink into the runner checkout (`mise/coverage.md`, row `argc`).
- **mise-plugin**: both define `SKOGAI_CONFIG_DIR`. Here it is a global `[env]` variable that "points at `~/skogai/config`, not this repo", with the meaning still to be decided (`PROJECT.md:163-164`); the plugin defaults it to `$XDG_CONFIG_HOME/skogai`, which is this repo's checkout path. See [mise-plugin](mise-plugin.md).
- **skogai2-cli**: `mise/dotfiles.md:131-132` records removing `config.skogai.toml` from the mise config on 2026-10-25, the file name skogai2-cli's settings layer uses. See [skogai2-cli](skogai2-cli.md).
- **Predecessors** (`SKOGAI.md:23-28`, `mise/old-dotfiles.md`, `shell/zsh.md:38-45`): stow dotfiles, then "ai-skogai", the rcm repo `SkogBackup/.dotfiles`, a chezmoi setup and the `skogansible` zsh role. This repo is "skogai config 3.0", started 2026-10-25.
- Other `SKOGAI_*` names recorded: `SKOGAI_DOCS_DIR`, `SKOGAI_CLAUDE_CODE_DOCS`, `SKOGAI_CLAUDE_CODE_DOCS_DIR` (global mise `[env]`), planned `SKOGAI_<GROUP>_DIR` per module (`PROJECT.md:159-177`), and legacy atuin vars `SKOGAI_OLLAMA_API`, `XDG_SKOGAI_CONFIG_DIR`, `XDG_SKOGAI_DIR` (`shell/atuin.md:23-25`).

## Gaps and stale references

- `secrets/fnox.md:124` says `claude-home/` is a submodule "here". No submodule is tracked; commit `b31ad3f` is titled "remove submodule".
- `containers/SKOGAI.md` has a route to `~/.config/containers/systemd/SKOGAI.md`, a file outside the repo. `bin/check-routes`, and so `bin/test full_test` and the `skogai routes` health check, can only pass on a machine that has that checkout.
- `PROJECT.md:36` says "Status as of 2026-10-25" but contains entries dated up to 2026-11-11. The mise pages mix dated snapshots (entry, file and checkpoint counts differ between `mise/SKOGAI.md`, `mise/dotfiles.md` and `PROJECT.md`); read each number with its date.
- `mise/coverage-triage.md` says it is deleted once every box is checked. Every box is checked and the file is still there.
- `mise/SKOGAI.md:96-97` notes that the pages cite `tmp/mise-docs/...`, a clone that no longer exists.
- `mise/SKOGAI.md:65` names the MCP server `skogai-mise`; `.mcp.json` and `.codex/config.toml` name it `mise`. `shell/atuin.md:51-54` says the atuin MCP setup changed on 2026-11-11 and needs a recheck.
- `PROJECT.md:17` gives `./secrets/{fnox,ssh,ssh-agent,mise}/` as the intended layout. Today the pages are flat files (`secrets/fnox.md`), and `machine/` exists while the planned `dotfiles/` group does not.
- `SKOGAI.md` has three `[@TODO:...]` placeholders (tool types, environment descriptions, more environments). `mise/dotfiles-upstream.md`, `secrets/fnox.md`, `containers/podman.md` and `agents/herdr.md` have no frontmatter, unlike the other pages.
- Open items the repo lists itself: no fresh-machine adopt has been run end to end and there is no standing test environment (`PROJECT.md:52-57`, `mise/adopt.md:150-157`); `[tasks.bootstrap]` assumes Omarchy; fish activates mise twice; an undeclared `dev.mise.gptme-server` unit still runs; pacman copies of mise and atuin shadow mise's own in non-interactive shells, which makes `agents/health` report a false `herdr-binary` failure from an agent's zsh tool shell (`machine/SKOGAI.md:40-51`); secrets are not yet moved into fnox; credentials that were captured in the dotfile history in October are treated as burned and the history rewrite is still the owner's open decision (`mise/dotfiles.md:124-159`).
- The two most recent commits are titled "."; what they changed was not examined beyond the tree at HEAD.
- `AGENTS.md` states that commits here carry no Co-Authored-By line, and contains the owner's git identity; that is a convention for anyone committing to this repo.
