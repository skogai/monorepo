---
type: concept
title: "The two orgs: which copy is live"
description: For each repo name that exists in both the skogai and skogai2 GitHub orgs, what each copy holds and which one the files show to be current, including the three repos named skogix and the dispute over the /skogai path.
tags: [orgs, duplicates, skogai2, canonical]
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - doc/surveys/2026-11-14-repo-survey.md
  - doc/pathfinder-2026-11-14/00-features.md
  - openwiki/repos/
---

# The two orgs: which copy is live

**Several names exist in both `github.com/skogai` and `github.com/skogai2`. In most cases the `skogai2` copy is the newer one, but no file declares a rule, and the owner has not settled it** (see [question 1.1 of the survey](../../doc/surveys/2026-11-14-repo-survey.md)). This page records what the trees show. In the catalog, a `skogai2` repo is named with the prefix `skogai2-`.

## Name by name

| Name | `skogai` copy | `skogai2` copy | What the files show |
|---|---|---|---|
| core | `core`, last commit 2026-10-24, not covered | [skogai2-core](../repos/skogai2-core.md), 2026-11-09 | `skogai2-core` was copied from `skogai/core` on 2026-10-24 and continues it. Its own docs still call it `skogai/core`. |
| dash-skogai | `dash-skogai`, dormant since 2026-09-20, not covered | [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md), 2026-11-01 | Same stated purpose, the shared `/skogai` workspace. The skogai2 copy is the one being worked on; its README describes paths that were deleted in October. |
| dot-skogai | [dot-skogai](../repos/dot-skogai.md), 623 files, quiet since 2026-09-27 | `skogai2-dot-skogai`, a three-file placeholder, not covered | The older repo holds all the content. Nothing in it mentions the skogai2 placeholder. |
| skogai-routing | `skogai-routing`, dormant, not covered | [skogai2-skogai-routing](../repos/skogai2-skogai-routing.md), version 0.1.0 | The skogai2 copy is a short restart of the convention. Copies of the older skill also sit in [skogai-core](../repos/skogai-core.md) and [harness](../repos/harness.md). |
| marketplace | `skogai/marketplace`, not in the catalog | [skogai2-marketplace](../repos/skogai2-marketplace.md), active | No shared commits; a reimplementation. The older marketplace role is also played by [skogai-core](../repos/skogai-core.md). |
| docs | [docs](../repos/docs.md), the knowledge archive | `skogai2-docs`, a Claude Code docs snapshot, not covered | Different collections that share a name. |
| skogai | `skogai`, a README placeholder, not covered | [skogai2-skogai](../repos/skogai2-skogai.md), the orchestration repo | Not duplicates. |
| skogix | [skogix](../repos/skogix.md), notes and backlog | [skogai2-skogix](../repos/skogai2-skogix.md), agent-config workspace | Different roles, no shared commits. A third `skogix` is a private fork under the owner's personal account. |

Repos that exist only in `skogai2`: [skogai2-config](../repos/skogai2-config.md), [skogai2-cli](../repos/skogai2-cli.md), [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md), [skogai2-skogai-fleet](../repos/skogai2-skogai-fleet.md).

## Who owns `/skogai`

Two repos assume they are checked out at `/skogai`:

- [skogai2-dash-skogai](../repos/skogai2-dash-skogai.md) hard-codes the path in its coordination scripts.
- [skogai2-skogix](../repos/skogai2-skogix.md) sets `CLAUDE_CONFIG_DIR=/skogai/claude` and `SKOGAI_CONFIG_DIR=/skogai/config` in its launchers.

The repos contradict each other. Decision 0005 in `skogai2-skogix` says `/skogai` is dash-skogai, the shared layer, and `~/.skogai` is dot-skogai, the user layer. Decision 0003 in the same repo places skogix at `~/skogix`. [skogai2-config](../repos/skogai2-config.md) says the origin of `/skogai` "is `skogai2/skogix` now". The Pathfinder inventory records an owner decision that `skogai2-dash-skogai` owns `/skogai`. Which repo sits at that path on the workstation today cannot be told from the repos.

## Copies inside other repos

Material is also duplicated by copying, not only by forking:

- The jq skill: canonical in [skogai-jq](../repos/skogai-jq.md); full copies remain in `skogai-core/todo/skills/skogai-jq` and in `harness/marketplace/plugins/skogix-hooks/skills/skogai-jq`.
- The `dot-core` plugin from dot-skogai: copied into `skogai-core/todo/` and `harness/marketplace/plugins/skogix-hooks/`.
- The owner documents under `skogix/`: in both [docs](../repos/docs.md) and `dot-skogai/docs/skogix/`, partly identical and partly diverged.
- `scripts/config` and `scripts/frontmatter` in [skogai2-marketplace](../repos/skogai2-marketplace.md) are copied from [skogai2-skogai-runner](../repos/skogai2-skogai-runner.md).
