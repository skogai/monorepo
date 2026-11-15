---
type: concept
title: "Shared concerns: which repo implements what"
description: A map from each concern that cuts across the SkogAI repos (settings, machine config, plugins, hooks, fleet control, orchestration, services, network edge, knowledge) to the repo that currently implements it and the older copies.
tags: [architecture, features, map, duplication]
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - doc/pathfinder-2026-11-14/00-features.md
  - openwiki/repos/
---

# Shared concerns: which repo implements what

**Most concerns have one repo that is being worked on and one or more older copies.** The table follows the feature numbering (F1 to F14) of the [Pathfinder inventory](../../doc/pathfinder-2026-11-14/00-features.md) and adds what the repo pages found. "Live" means the copy with recent commits, not that it is finished: several live copies are specifications or stubs.

| Concern | Live | Older or parallel copies | State of the live copy |
|---|---|---|---|
| F1 Fleet control and repo registry | [skogai2-core](../repos/skogai2-core.md) | `core`; gita lists in several repos; `mani.yaml` in the monorepo | Root CLI is mostly stubs. A `repo` module and a workorder design are the live parts. It uses gita and never mentions mani. |
| F2 Settings and `SKOGAI_*` environment | [mise-plugin](../repos/mise-plugin.md) | [skogai2-cli](../repos/skogai2-cli.md) `bin/config`; `scripts/config` in [skogai2-marketplace](../repos/skogai2-marketplace.md); `best-argc-version/` in [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md) | Plugin is small, tested and pinned by the monorepo. The CLI's HEAD has hard-coded debug defaults. |
| F3 Machine config, dotfiles, secrets | [skogai2-config](../repos/skogai2-config.md), [nvim-omarchy](../repos/nvim-omarchy.md) | `skogai-nov10` | Config repo holds documentation and health checks. The dotfiles are in a separate private repo. |
| F4 `/skogai` shared workspace | [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md) | `dash-skogai`; [skogai2-skogix](../repos/skogai2-skogix.md) claims the same path | Admin scripts exist. The launcher generator depends on a removed directory. |
| F5 `.skogai` folder and routing files | [skogai2-skogai-routing](../repos/skogai2-skogai-routing.md) | `skogai-routing`; [dot-skogai](../repos/dot-skogai.md); copies in [skogai-core](../repos/skogai-core.md) and [harness](../repos/harness.md) | Documentation only, version 0.1.0, no validator. A type system for `.skogai/` is drafted in [skogai2-skogai](../repos/skogai2-skogai.md). |
| F6 Plugin marketplace | [skogai2-marketplace](../repos/skogai2-marketplace.md) | [skogai-core](../repos/skogai-core.md); a marketplace in [skogai2-skogix](../repos/skogai2-skogix.md) and in [harness](../repos/harness.md) | One local plugin and five external entries. The manifest is generated and checked for drift. |
| F7 Hook runtime and session journal | `plugins/skogai-core` in [skogai2-marketplace](../repos/skogai2-marketplace.md) | four earlier attempts in [harness](../repos/harness.md); `dot-core` | 13 hook events, all off by default. It writes `.skogai/journal.md` and `.skogai/logs/skogai-core/`. |
| F8 jq transform skill | [skogai-jq](../repos/skogai-jq.md) | copies in `skogai-core/todo/` and `harness` | 70 transforms. Live install into a harness is untested by its own account. |
| F9 Agent orchestration and work orders | [skogai2-skogai](../repos/skogai2-skogai.md) | workorder design in [skogai2-core](../repos/skogai2-core.md), in a different format; [skogai2-skogai-fleet](../repos/skogai2-skogai-fleet.md) | A spec and delegation rules. One completed work order, none open. |
| F10 Command runner | [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md) | its own `best-argc-version/` | Reset on 2026-11-07. One live source file, a read-only log reader. |
| F11 Service runtime | [podman](../repos/podman.md) | `systemd` (not in the catalog); `old-systemd-solution/` in [cloudflare](../repos/cloudflare.md) | Four services with hourly health checks and nightly backups. |
| F12 Cloudflare and network edge | [cloudflare](../repos/cloudflare.md) | none | Scripts are dry-run unless told to apply. Four inventory notes are marked stale by the repo. |
| F13 Knowledge, memory, decisions | `.skogai/` folders of the skogai2 repos | [dot-skogai](../repos/dot-skogai.md), [docs](../repos/docs.md), `wiki`, per-repo `openwiki/` folders | Split across repos. No single store. |
| F14 Claude Code docs mirror | `plugins/skogdocs` in [skogai2-skogix](../repos/skogai2-skogix.md) | `skogai2-docs`; a 223-file snapshot in [skogai2-marketplace](../repos/skogai2-marketplace.md); a download script in [skogai-core](../repos/skogai-core.md) | Offline lookup plugin with tests. |

## Dependencies between the live repos

- [mise-plugin](../repos/mise-plugin.md) is consumed by the monorepo (`mise.toml`, pinned by commit in `.config/mise/conf.d/plugin.skogai.toml`).
- [skogai2-marketplace](../repos/skogai2-marketplace.md) supplies the `skogai-core` plugin that [skogai2-skogai](../repos/skogai2-skogai.md) and [skogai2-skogix](../repos/skogai2-skogix.md) enable. Its journal and log files show up in most repos.
- [skogai2-core](../repos/skogai2-core.md)'s `repo` module is built to plug into the runner's module commands, which the runner deleted in its reset.
- [skogai2-skogix](../repos/skogai2-skogix.md) carries `skogai-runner` and `skogai-routing` as submodules.
- [skogai2-config](../repos/skogai2-config.md) wraps [podman](../repos/podman.md)'s health check and declares the other repos' checkout paths as bootstrap repos.
- [podman](../repos/podman.md) and [cloudflare](../repos/cloudflare.md) act on the same Cloudflare account and the same tunnel, from two repos. Their notes on which hostname sits behind which tunnel disagree in one place (see the cloudflare page).
