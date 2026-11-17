---
type: concept
title: "Shared concerns: which repo owns what"
description: A map from the seven Pathfinder systems (S1 ENV to S7 SERVICES) to the repo the unified proposal names as owner of each concern (U1 to U9), the older copies, and the state of the owner repo as read on 2026-11-15.
tags: [architecture, systems, map, duplication]
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - doc/pathfinder-2026-11-14/00-features.md
  - doc/pathfinder-2026-11-14/03-unified-proposal.md
  - openwiki/repos/
---

# Shared concerns: which repo owns what

**The architecture vocabulary is Pathfinder's, not this wiki's.** [00-features.md](../../doc/pathfinder-2026-11-14/00-features.md), Revision 1, groups the repos into seven systems, S1 to S7. [03-unified-proposal.md](../../doc/pathfinder-2026-11-14/03-unified-proposal.md) names one owner per concern, U1 to U9, and a retirement list. This page maps those onto the repo pages and adds the state each owner repo was in when read. The proposal is the authority: where a line here and the proposal differ, the proposal wins. The older F1 to F14 numbering is superseded and not used here.

"Owner" means the repo the proposal names. It does not mean finished: several owners are specifications or stubs.

## By system

| System | Owner per the proposal | Other copies | State of the owner as read |
|---|---|---|---|
| **S1 ENV**: environment and settings plane | U1: [mise-plugin](../repos/mise-plugin.md) is the only thing that computes SkogAI env. [skogai2-cli](../repos/skogai2-cli.md) is the one get/set/list CLI. [skogai2-config](../repos/skogai2-config.md) and [nvim-omarchy](../repos/nvim-omarchy.md) hold the workstation and human-home levels. | `scripts/config` in [skogai2-marketplace](../repos/skogai2-marketplace.md) (U1: delete, uncalled copy); `best-argc-version/` in the runner (frozen); `skogai-nov10` | Plugin: small, tested, version 0.2.0, pinned by the monorepo. CLI: HEAD has hard-coded debug defaults that contradict its docs and tests. Config: documentation and health checks, active. |
| **S2 RUN**: execution plane | U5: the work-order format is the spec in [skogai2-skogai](../repos/skogai2-skogai.md); execution is `orchestrate-worktrees.js` in [harness](../repos/harness.md). U3: commands are mise tasks, in every repo. Routing: [skogai2-skogai-routing](../repos/skogai2-skogai-routing.md), checked by `bin/check-routes` in skogai2-config. Runner: [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md). | `skogai-routing` (retiring); a different work-order format in [skogai2-core](../repos/skogai2-core.md) and in the runner's `WORKORDERS.md`; personas in [skogai2-skogai-fleet](../repos/skogai2-skogai-fleet.md) | Spec and delegation rules exist; one completed work order, none open. Runner was reset on 2026-11-07 and has one live source file. Routing is documentation only, version 0.1.0. `mise run wo:dispatch` is proposed, not built. |
| **S3 DASH**: `/skogai` shared ground and agent homes | U2: [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md). Agent identity is the unix uid. | [skogai2-skogix](../repos/skogai2-skogix.md) launchers (to be replaced by one `skogai-agent` launcher; its `/skogai` claim is stale); `dash-skogai` (retiring) | Admin scripts exist. The launcher generator depends on a removed directory, and the README describes deleted paths. |
| **S4 DOT**: `.skogai` base config, bootstrap, knowledge | U7: `skogai2-dot-skogai`, as the layout doc and the bootstrap submodule. Not covered by this wiki: it is a three-file placeholder. | [dot-skogai](../repos/dot-skogai.md) (old generation); [docs](../repos/docs.md) and `wiki` (archives); the `.skogai/` folders of the skogai2 repos; per-repo `openwiki/` folders | The owner repo is empty. The live layout to copy in is in skogai2-skogai. Open owner calls (W20): whether old knowledge, memory and journal migrate or freeze, one decision store, and **OpenWiki: revive or delete**, which decides the future of this wiki too. |
| **S5 FLEET**: repo registry and control plane | U4: the monorepo's `mani.yaml`, through mise tasks. | [skogai2-core](../repos/skogai2-core.md) (`repo` module and gita lists; U4: read mani or retire); `core` (retiring) | The catalog is live. skogai2-core's root CLI is mostly stubs; its contracts are the part the proposal wants kept. It uses gita and never mentions mani. |
| **S6 PLUGINS**: marketplace, hooks, skills, docs lookup | U8: [skogai2-marketplace](../repos/skogai2-marketplace.md) is the only registered marketplace. U6: its `skogai-core` plugin owns the repo-level hook journal (decided 2026-11-15), with the journal at `doc/journal.md`. [skogai-jq](../repos/skogai-jq.md) is the canonical jq skill. Docs lookup: `skogdocs` in [skogai2-skogix](../repos/skogai2-skogix.md). | [skogai-core](../repos/skogai-core.md) and `marketplace` (retiring); four earlier hook attempts and copies in [harness](../repos/harness.md); `skogai2-docs` and the marketplace's `docs/` snapshot (owner call) | Marketplace: one local plugin, five external entries, manifest generated and drift-checked. Hook runtime: 13 events, off by default; its default journal path is still `.skogai/journal.md`. jq: 70 transforms, live harness install untested by its own account. |
| **S7 SERVICES**: runtime services and edge | U9: [podman](../repos/podman.md) for services, `mise run health` to `skogai2-config/bin/health` for health. Edge: [cloudflare](../repos/cloudflare.md). | `systemd` (retiring, not in this wiki); `cloudflare/old-systemd-solution/` and `cloudflare/pangolin/` (U9: delete and retire) | podman: four services with hourly health checks and nightly backups. cloudflare: scripts are dry-run unless told to apply; four inventory notes are marked stale by the repo. |

## Coupling between systems

From Revision 1 of the inventory, with what the repo pages confirm:

- **S1 to S2**: the runner consumes the env. [skogai2-core](../repos/skogai2-core.md)'s `repo` module is built to plug into the runner's module commands, which the runner deleted in its reset.
- **S3 and S4**: dash is the shared ground, dot is the per-project config. Both owner repos are thin today.
- **S5 to S2**: the registry feeds worktrees and work orders. [skogai2-skogix](../repos/skogai2-skogix.md) carries `skogai-runner` and `skogai-routing` as submodules.
- **S6 to S4**: the hooks write the journal. The plugin's journal and log files show up in most repos' `.skogai/` folders.
- **S1 to S7**: [skogai2-config](../repos/skogai2-config.md) wraps [podman](../repos/podman.md)'s health check. podman and [cloudflare](../repos/cloudflare.md) act on the same Cloudflare account and tunnel from two repos, each pinning the account id (U1: move it into one mise `[env]`).

## Retirement list

The proposal retires `core`, `dash-skogai`, `marketplace`, `skogai-core`, `skogai-routing`, `skogai-nov10`, `systemd` and `cloudflare/old-systemd-solution/`: archive, not delete, pending owner sign-off. Of these only [skogai-core](../repos/skogai-core.md) has a page here, marked as retiring.
