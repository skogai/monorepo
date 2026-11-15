---
type: concept
title: Shared conventions
description: The conventions several SkogAI repos share (router files and routes blocks, the .skogai folder, SKOGAI_ variables, mise and argc tooling, workstation path assumptions), with where each one is defined and where it varies.
tags: [conventions, routing, dot-skogai, environment, tooling]
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - openwiki/repos/
---

# Shared conventions

**The repos share habits more than code.** None of these conventions is enforced across repos. Each is described where it is defined, then where it varies.

## Router files

A router is a Markdown file with an all-caps name whose job is to point at other files. The convention is defined in [skogai2-skogai-routing](../repos/skogai2-skogai-routing.md): `SKOGAI.md` is the single entry point, and a `<routes>` block lists `@./path` links. Ownership is one hop and not transitive.

- `AGENTS.md` is often a symlink to `SKOGAI.md`, and `CLAUDE.md` contains only a pointer to it ([skogai2-core](../repos/skogai2-core.md), [harness](../repos/harness.md), [dot-skogai](../repos/dot-skogai.md), [podman](../repos/podman.md)). In [skogai2-skogai](../repos/skogai2-skogai.md) every `CLAUDE.md` is only `@AGENTS.md`, as in the monorepo.
- Frontmatter carries `type` (`router` or `routing`) and often `permalink: <repo>/<name>`.
- Routes rot. Broken or self-referring routers are recorded for [docs](../repos/docs.md), [harness](../repos/harness.md), [dot-skogai](../repos/dot-skogai.md) and [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md).
- Only [skogai2-config](../repos/skogai2-config.md) has a checker, `bin/check-routes`.
- The monorepo's `agents/<name>.md` cache copies a repo's root `AGENTS.md`. A repo whose entry file is `SKOGAI.md`, `CLAUDE.md` or `AGENT.md` has no cached copy, and a cached copy can outlive the file: `agents/skogai2-skogai-fleet.md` is a copy of a file deleted on 2026-11-15.

## The `.skogai/` folder

`.skogai/` is a per-repo folder for agent state. What it holds differs by generation.

- **Older**: [dot-skogai](../repos/dot-skogai.md) was the folder itself, shared into other repos as a submodule and later by symlink, with `knowledge/`, `memory/`, `journal/` and a toolchain.
- **Current**: a mix of committed and runtime files. Common entries are `journal.md` (the turn journal the `skogai-core` plugin appends to), `logs/<plugin>/log.jsonl`, `tmp/` for state, `todo` files, `rules/`, `memory/`, `decisions/` and `modules/`.
- [skogai2-cli](../repos/skogai2-cli.md) defines `.skogai/base/<path>` as the committed default and `.skogai/<path>` as the override.
- Whether the journal and logs are tracked varies by repo. Hook logs hold raw tool output, so check before committing them.

## `SKOGAI_*` variables

There is no single registry. The names found, by where they are set:

| Variables | Set or defined in |
|---|---|
| `SKOGAI_MONOREPO_DIR`, `SKOGAI_CONFIG_DIR`, `SKOGAI_HOST`, `SKOGAI_OS`, `SKOGAI_ARCH` | [mise-plugin](../repos/mise-plugin.md) |
| `SKOGAI_CONFIG_{SYSTEM,GLOBAL,BASE,LOCAL}_FILE`, `SKOGAI_CONFIG_PREFIX`; key `core.debug` maps to `SKOGAI_CORE_DEBUG` | [skogai2-cli](../repos/skogai2-cli.md) |
| `SKOGAI_SYSTEM_DIR`, `SKOGAI_CONFIG_DIR`, `SKOGAI_LOCAL_DIR`, `SKOGAI_MODULE_PATH`, `SKOGAI_<KEY>` overrides | `scripts/config` in [skogai2-marketplace](../repos/skogai2-marketplace.md), from the runner |
| `SKOGAI_LOG`, and in the kept argc version `SKOGAI_MODULE_DIR`, `SKOGAI_BIN`, `SKOGAI_RUNNER_*`, `SKOGAI_MEMORY_*` | [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md) |
| `SKOGAI_USER`, `SKOGAI_MODE` (derived from Claude Code variables) | [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md) |
| `SKOGAI_REPO_GROUP`, `SKOGAI_REPO_HOME`, `SKOGAI_MARKETPLACE_*`, `SKOGAI_CLAUDE_PLUGIN_*`, `SKOGAI_AGENT_NAME` | [skogai2-core](../repos/skogai2-core.md) |
| `SKOGAI_DOCS_DIR`, `SKOGAI_CLAUDE_CODE_DOCS_DIR`, `SKOGAI_HEALTH_ROOT` | [skogai2-config](../repos/skogai2-config.md) |
| `SKOGAI_ROOT`, `SKOGAI_HOME`, `SKOGAI_DOCS`, `SKOGAI_TEMP` | older repos: [dot-skogai](../repos/dot-skogai.md), [docs](../repos/docs.md) |

`SKOGAI_CONFIG_DIR` means different things in different repos: `$XDG_CONFIG_HOME/skogai` by default in the plugin, `/skogai/config` in the skogix launchers, `.skogai/config` in dot-skogai, and a per-namespace value in skogai2-skogai. [skogai2-config](../repos/skogai2-config.md) records that its meaning is undecided.

## Tooling

- **mise** is the task and environment layer in the current repos. The runner's 2026-11-06 decision is `usage` plus mise for interfaces.
- **argc** (`Argcfile.sh`) drives the older CLIs: [skogai2-core](../repos/skogai2-core.md), the kept runner version, [podman](../repos/podman.md)'s `bin/` scripts. The runner calls it frozen.
- **gita** tracks the fleet in [skogai2-core](../repos/skogai2-core.md) and in decision 0003 of skogai2-skogix. The monorepo uses **mani**. The two are not reconciled.
- **Bats** for shell tests; **hk** with shellcheck and shfmt for hooks; **worktrunk** (`wt`) for worktrees; **herdr** for agent sessions; **fnox** with age for secrets, planned in podman and present in dash-skogai.
- **OKF** frontmatter (`type`, `status`) is the type tag in the skogai2 repos, validated with `okn`.

## Workstation assumptions

Many repos only work at a fixed path on the owner's machine. The ones the pages record:

| Path | Repo expected there |
|---|---|
| `~/.config/skogai` | skogai2-config |
| `~/.config/containers/systemd` | podman |
| `~/.config/nvim` | nvim-omarchy |
| `/skogai` | skogai2-dash-skogai or skogai2-skogix (disputed, see [orgs and copies](orgs-and-copies.md)) |
| `~/skogai` | skogai2-skogai |
| `~/.local/src/<repo>` | gita-tracked repos, including cloudflare and the skills that dot-skogai symlinks to |
| `~/Work` | the monorepo |

A fresh clone elsewhere will find broken symlinks and absolute paths in [dot-skogai](../repos/dot-skogai.md), [harness](../repos/harness.md), [skogai2-core](../repos/skogai2-core.md) and [skogai2-skogai](../repos/skogai2-skogai.md).
