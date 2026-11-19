---
type: quickstart
title: Quickstart
description: A routing page for the SkogAI repos wiki, giving the page to open for each kind of question and the commands that fetch a repo.
tags: [quickstart, routing, catalog]
generated: { by: "claude-code", at: "2026-11-15" }
---

# Quickstart

**The monorepo holds a catalog, not code.** The repos are separate. This wiki describes the active ones so you can pick the right one before cloning it.

## Which page for which question

| Question | Open |
|---|---|
| What is repo X and is it still used? | `repos/<name>.md`, listed in [repos/index.md](repos/index.md) |
| The name exists in both `skogai` and `skogai2`. Which one is live? | [concepts/orgs-and-copies.md](concepts/orgs-and-copies.md) |
| Which repo handles settings, hooks, plugins, services, fleet control? | [concepts/shared-concerns.md](concepts/shared-concerns.md) |
| What are `SKOGAI.md`, `<routes>`, `.skogai/`, `SKOGAI_*`? | [concepts/conventions.md](concepts/conventions.md) |
| Where is old knowledge: personas, lore, decisions, journals? | [repos/docs.md](repos/docs.md) and [repos/dot-skogai.md](repos/dot-skogai.md) |
| Why is repo Y not in this wiki? | [repos/index.md](repos/index.md), "Not covered" |
| Repo Y was archived. What replaced it? | [repos/retired.md](repos/retired.md) |

## Where to start by task

- **Environment and settings**: [mise-plugin](repos/mise-plugin.md) sets the base `SKOGAI_*` variables. [skogai2-config](repos/skogai2-config.md) documents the workstation setup. [skogai2-cli](repos/skogai2-cli.md) is an unfinished layered-config CLI.
- **Claude Code plugins and hooks**: [skogai2-marketplace](repos/skogai2-marketplace.md) is the live marketplace and holds the hook runtime. [skogai-jq](repos/skogai-jq.md) is the jq skill.
- **Services and network edge**: [podman](repos/podman.md) for the containers on the workstation, [cloudflare](repos/cloudflare.md) for tunnels, DNS and Access.
- **Agent workspaces and orchestration**: [skogai2-skogai](repos/skogai2-skogai.md), [skogai2-dash-skogai](repos/skogai2-dash-skogai.md), [skogai2-skogix](repos/skogai2-skogix.md), [skogai2-core](repos/skogai2-core.md).
- **Retired repos and their old wikis**: [retired](repos/retired.md).

## Fetch a repo

```sh
mani sync -t <name> --ignore-sync-state      # one repo, into repos/<name>/
mani sync -t openwiki --ignore-sync-state    # the repos this wiki covers
mise run openwiki:clone                      # the same, as a mise task
```

Six of the covered repos are private (`cloudflare`, `podman`, `nvim-omarchy`, `docs`, `dot-skogai`, `skogai2-core`) and need credentials to clone.

## Limits of this wiki

- Pages were written by reading. No command, test or install step in them was run.
- The clones were shallow (50 commits), so history before that is not described.
- Large archives and vendored trees are covered at overview depth. Each page says what was not read.
- The pages are hand-written in the OpenWiki layout. They carry no OpenWiki claim files, so the first run of the [update workflow](../.github/workflows/openwiki-update.yml) will regenerate them from [INSTRUCTIONS.md](INSTRUCTIONS.md).
