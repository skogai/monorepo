---
type: index
title: Repo pages
description: The catalog repos this wiki covers, grouped by role, and the catalog repos it leaves out with the reason for each.
tags: [index, repositories, catalog]
generated: { by: "claude-code", at: "2026-11-15" }
---

# Repo pages

State is as of each page's recorded commit. "Last commit" is the date of the cloned HEAD.

## Environment and configuration

| Repo | Last commit | What it is |
|---|---|---|
| [mise-plugin](mise-plugin.md) | 2026-11-13 | mise environment plugin (Lua) that sets the base `SKOGAI_*` variables. Version 0.2.0, pinned by the monorepo. |
| [skogai2-config](skogai2-config.md) | 2026-11-15 | Knowledge and health-check repo for the workstation configuration. Active. |
| [skogai2-cli](skogai2-cli.md) | 2026-10-24 | Clean-room rework of the skogai CLI; only the config module exists. Quiet. |
| [nvim-omarchy](nvim-omarchy.md) | 2026-11-13 | Personal Neovim configuration on LazyVim as Omarchy ships it. Private. Personal side project, set aside (2026-11-19). |

## Plugins, skills and hooks

| Repo | Last commit | What it is |
|---|---|---|
| [skogai2-marketplace](skogai2-marketplace.md) | 2026-11-13 | Live Claude Code marketplace with the `skogai-core` hook runtime plugin. Active. |
| [skogai-jq](skogai-jq.md) | 2026-11-14 | Skill with 70 jq transforms, each with schema, test and fixtures. Canonical copy. |
| [skogai-core](skogai-core.md) | 2026-09-11 | Older marketplace around the routing skill, with a large unmigrated `todo/` tree. **Archived 2026-11-19**; kept as a map, see [retired repos](retired.md). |
| [skogai2-skogai-routing](skogai2-skogai-routing.md) | 2026-10-31 | The routing-file convention, version 0.1.0. Documentation only. |
| [harness](harness.md) | 2026-11-09 | Overview workspace for the harness rebuild; about 85% vendored or copied material. |

## Workspaces, orchestration and fleet

| Repo | Last commit | What it is |
|---|---|---|
| [skogai2-skogai](skogai2-skogai.md) | 2026-11-10 | Orchestration repo: herdr work orders, the dash type-system draft, rules and memory. Mostly specifications. |
| [skogai2-dash-skogai](skogai2-dash-skogai.md) | 2026-11-01 | The repo meant to live at `/skogai` as the shared multi-agent workspace. Work in progress. |
| [skogai2-skogix](skogai2-skogix.md) | 2026-11-09 | The owner's agent-config workspace built for `/skogai`. Work in progress. |
| [skogai2-core](skogai2-core.md) | 2026-11-09 | Bash/argc control plane for the repo fleet, continued from `skogai/core`. Work in progress. Private. |
| [skogai2-skogai-runner](skogai2-skogai-runner.md) | 2026-11-09 | Bash command runner, mid-remake; one live source file after a deliberate reset. |
| [skogai2-skogai-fleet](skogai2-skogai-fleet.md) | 2026-11-15 | Stripped copy of the Nelson orchestration skill plus six vendored projects. |
| [skogix](skogix.md) | 2026-11-14 | The owner's notes and backlog repo. No code. Personal side project, set aside (2026-11-19). |

## Services and network

| Repo | Last commit | What it is |
|---|---|---|
| [podman](podman.md) | 2026-11-14 | Rootless Podman Quadlets for one workstation, with health checks and backups. Active. Private. |
| [cloudflare](cloudflare.md) | 2026-11-13 | Ops repo for one Cloudflare account: tunnels, DNS, Access. Active. Private. |

## Knowledge archives (overview depth)

| Repo | Last commit | What it is |
|---|---|---|
| [docs](docs.md) | 2026-10-06 | 2,536-file archive of personas, memory blocks, lore, governance and journals. Frozen (2026-11-19). Private. |
| [dot-skogai](dot-skogai.md) | 2026-09-27 | Older shared agent workspace: routers, knowledge, memory, journal. Frozen (2026-11-19), mid-migration. Private. |

## Not covered

The repos archived on 2026-11-19 are on [retired repos](retired.md). These catalog repos have no page. The reason comes from the [2026-11-14 repo survey](../../doc/surveys/2026-11-14-repo-survey.md) and the [Pathfinder feature inventory](../../doc/pathfinder-2026-11-14/00-features.md), not from a fresh read.

| Repo | Reason |
|---|---|
| wiki | Stubs, dormant since 2026-05-28. |
| skogai | One-commit README placeholder. |
| skogai2-dot-skogai | Placeholder: three files, "nothing built yet". |
| repomix | Fork of an upstream project; the owner's commits are merges. |
| skogai2-aliasflare | Fork of an upstream Cloudflare Workers project. It is a submodule of `cloudflare`. |
| skogai2-docs | Snapshot of the Claude Code documentation. Frozen (2026-11-19). |
| skogai2-skogpunk | Android game prototype, unrelated to the tooling. Personal side project, set aside (2026-11-19). |
| skogfleet | Not surveyed. The catalog entry points at `skogai2/skogfleet`, created 2026-11-15. |
| skogai-skogfleet | `skogai/skogfleet`, last pushed 2026-07-23. Not surveyed. |
| skogai-events | Added 2026-11-19; the owner names it as the remake of the archived `skogai/marketplace`, currently a single plugin. Not surveyed. |

To add a repo, tag it `openwiki` in `mani.yaml` and write or regenerate its page.
