---
type: repository
title: skogai2-skogai-fleet
description: A stripped copy of the Nelson multi-agent orchestration skill (one skill file and 50 reference documents) with its helper scripts replaced by TODO placeholders, plus six vendored third-party projects under inspiration/. Reshaped on 2026-11-15; no entry file or runnable code of its own.
tags: [orchestration, multi-agent, skill, nelson, vendored, work-in-progress]
repo: skogai2/skogai-fleet
commit: d5f9464
last_commit: 2026-11-15
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-skogai-fleet/.NELSON-SKILL.md
  - repos/skogai2-skogai-fleet/references/crew-roles.md
  - repos/skogai2-skogai-fleet/references/squadron-composition.md
  - repos/skogai2-skogai-fleet/references/tool-mapping.md
  - repos/skogai2-skogai-fleet/references/structured-data.md
  - repos/skogai2-skogai-fleet/references/workflow-doctrine.md
  - repos/skogai2-skogai-fleet/inspiration/mise.toml
  - repos/skogai2-skogai-fleet/inspiration/backpass/README.md
  - repos/skogai2-skogai-fleet/inspiration/captains-deck/README.md
  - repos/skogai2-skogai-fleet/inspiration/captains-deck/herdr-plugin.toml
  - repos/skogai2-skogai-fleet/inspiration/dotfiles/README.md
  - repos/skogai2-skogai-fleet/inspiration/gnhf/README.md
  - repos/skogai2-skogai-fleet/inspiration/treehouse/README.md
  - repos/skogai2-skogai-fleet/inspiration/kun/README.md
  - agents/skogai2-skogai-fleet.md
---

# skogai2-skogai-fleet

**skogai-fleet is a working copy of the Nelson skill, a Royal Navy themed procedure for orchestrating several coding agents, kept together with a folder of vendored third-party projects used as inspiration.** Of 2,282 tracked files, 2,227 are vendored under `inspiration/`. The repo's own material is 51 Markdown files (`.NELSON-SKILL.md` and `references/`) and four PNG images. State: work in progress and in flux. Two commits on 2026-11-15 deleted the crew personas, `SKOGAI.md`, `AGENTS.md`, `TODO.md`, `.skogai/config` and `.old-references/` (35 files, 3,702 lines), so HEAD has no entry file, no README and no code. Before that the last change was 2026-10-24.

## Source map

Own versus vendored, from `git ls-files | cut -d/ -f1-2 | sort | uniq -c`:

| Path | Files | Holds |
|---|---|---|
| `.NELSON-SKILL.md` | 1 | Own. The skill: 471 lines, an eight-step mission workflow. Hidden dotfile name, so it is not picked up as a `SKILL.md`. |
| `references/*.md` | 11 | Own. Doctrine: `crew-roles`, `squadron-composition`, `tool-mapping`, `structured-data` (807 lines), `workflow-doctrine`, `the-estimate`, `action-stations`, `goal-alignment`, `model-selection`, `royal-marines`, `commendations`. |
| `references/admiralty-templates/` | 11 | Own. Document templates: sailing orders, estimate, battle plan, ship manifest, crew briefing, quarterdeck report, damage report, turnover brief, red-cell review, marine deployment brief, captain's log. |
| `references/standing-orders/` | 17 | Own. One file per named anti-pattern (for example `admiral-at-the-helm`, `split-keel`, `wrong-ensign`). |
| `references/damage-control/` | 11 | Own. Recovery procedures (for example `man-overboard`, `session-resumption`, `hull-integrity`, `circuit-breakers`). |
| `ChatGPT Image Nov 15, 2026, *.png` | 4 | Four generated images at the repo root, about 3.4 MB each. Not referenced by any file. |
| `inspiration/kun/` | 1,670 | Vendored. An Agent Skills package, "/kun"; 1,661 of the files are dated post archives in `content/`. |
| `inspiration/backpass/` | 182 | Vendored. npm package `backpass` 0.1.35, "Gradient descent for your agent memory". |
| `inspiration/treehouse/` | 156 | Vendored. Go tool managing a pool of reusable git worktrees for agents. |
| `inspiration/gnhf/` | 125 | Vendored. npm package `gnhf` 0.1.51, "good night, have fun": runs agents unattended. |
| `inspiration/captains-deck/` | 54 | Vendored. A read-only kanban plugin for Herdr showing a Firstmate agent flow (plugin id `herdr-firstmate-flow`, 0.10.0). |
| `inspiration/dotfiles/` | 39 | Vendored. A personal Mac setup using nix-darwin and home-manager. |
| `inspiration/mise.toml` | 1 | Own. Tools for building the vendored projects: `astro`, `go`, `pnpm`, `task`, `ttyd`, `vhs`, all `latest`. |

The vendored trees are plain copied files, not submodules. Five of them (`kun`, `backpass`, `treehouse`, `gnhf`, `dotfiles`) come from the same upstream GitHub account per their READMEs; `captains-deck` from another. I read only their READMEs and manifests.

## How it works

### The skill

`.NELSON-SKILL.md` has skill frontmatter (`name: nelson`, an `argument-hint`, `paths: [".state/**"]`) and tells the agent, acting as "admiral", to run eight steps:

1. **Issue Sailing Orders** (`:16`): outcome, metric, deadline, constraints, out of scope, stop criteria. Creates a mission directory `.state/missions/{YYYY-MM-DD_HHMMSS}_{SESSION_ID}/`.
2. **Conduct The Estimate** (`:74`): an optional seven-question analysis, partly delegated to sub-agents, with two user checkpoints.
3. **Draft Battle Plan** (`:102`): tasks, owners, dependencies, file ownership; written to `{mission-dir}/battle-plan.md`.
4. **Form the Squadron** (`:141`): choose an execution mode and assign each task a captain and ship.
5. **Get Permission to Sail** (`:248`): the user approval gate.
6. **Run Quarterdeck Rhythm** (`:265`): checkpoints, progress and context-budget ("hull integrity") tracking, shutting down finished agents.
7. **Set Action Stations** (`:319`): risk tiers and verification, including a red-cell review.
8. **Stand Down And Log Action** (`:336`): captain's log and mission summary.

Two lookup tables follow: Standing Orders (`:421`, 17 situations to files) and Damage Control (`:445`, 11 situations to files). Every reference path named in the skill exists under `references/`.

### Execution modes and tools

`references/squadron-composition.md` defines five modes: `single-session`, `subagents`, `agent-team`, `workflow`, `hybrid-workflow`, with a decision matrix; an explicit user choice overrides it. `references/tool-mapping.md` maps each operation to a Claude Code tool by mode (`TeamCreate`, `Agent`, `TaskCreate`, `TaskUpdate`, `SendMessage`, `/goal`). `references/crew-roles.md` caps a ship at four crew and gives a crew-or-direct decision list. `references/workflow-doctrine.md` covers Claude Code dynamic workflows and states that Nelson produces the charter and gates but does not compile or invoke workflow scripts.

### What is missing: the helper scripts

The skill depends on two helpers, `nelson-data` and `nelson-phase`, for all structured state: mission init and recovery, task and squadron registration, checkpoints, events, handoff packets, phase advances, stand-down. In this copy every call has been replaced by a placeholder: 60 occurrences of `TODO(script:nelson-data)` and 12 of `TODO(script:nelson-phase)` across the skill and references, each marked "not built yet". `references/structured-data.md:3` says the helper is not built and "its location is undecided", while still documenting its subcommands and JSON files (`sailing-orders.json`, `mission-log.json`, `fleet-status.json`). No script, hook or agent definition is tracked. The procedure can only be followed as prose, with the JSON capture and phase validation skipped.

## How to use it

The repo defines no commands, tasks or install steps of its own. There is no plugin manifest and no `SKILL.md` at a path a skill loader would find.

- To read the procedure: open `.NELSON-SKILL.md` and follow its `references/` links.
- To use it as a skill it would have to be copied to a skill folder as `SKILL.md` alongside `references/`. That is an inference from the frontmatter, not something the repo documents.
- `inspiration/mise.toml` installs build tools for the vendored projects when `mise install` is run in that folder. Each vendored project has its own README and build files.
- Runtime assumptions inside the skill: Claude Code with sub-agent and agent-team tools, a writable `.state/` directory in the working repo, and the `gh` CLI for an optional prompt (`.NELSON-SKILL.md:359`) that offers to star the upstream Nelson repository.

## Relations to other SkogAI repos

- **Upstream Nelson.** The skill names its canonical repository as `harrymunro/nelson` (`.NELSON-SKILL.md:359`). This repo is a modified copy, not SkogAI-original text; no licence file or import revision is recorded.
- **skogai-routing convention.** The cached `agents/skogai2-skogai-fleet.md` in the monorepo is the deleted `AGENTS.md`: a `type: router` file with a `<routes>` block pointing at `@SKOGAI.md`. Both files were removed on 2026-11-15, so the cache is stale.
- **Herdr.** `inspiration/captains-deck` is a Herdr plugin. The monorepo survey describes `skogai2-skogai` as an orchestration workspace using Herdr; nothing in this repo links to it directly.
- **Earlier contents, per git history.** A `hook-tap` plugin and marketplace manifest (added 2026-10-04, removed 2026-10-10), old Claude plugins (removed 2026-10-17), and `crew/` personas generated from a `PERSONAS.md` (added 2026-10-17, removed 2026-11-15). The monorepo survey's description, "persona redesign of the Nelson plugin", matches the pre-2026-11-15 tree, not HEAD. `hook-tap` is also named in the `skogai-routing` `.gitignore`.
- No `SKOGAI_*` variables and no paths into other SkogAI repos appear in the own files.

## Gaps and stale references

- No README, `SKOGAI.md`, `AGENTS.md` or `TODO.md` at HEAD. Nothing states what the repo is for or what the plan is after the 2026-11-15 deletions.
- `nelson-data` and `nelson-phase` are unbuilt; 72 placeholders mark where they go. One more, `TODO(script:nelson_data_patterns)` (`.NELSON-SKILL.md:423`), marks a missing pattern-mining workflow.
- The skill file is a hidden dotfile (`.NELSON-SKILL.md`), so it is inert as a skill.
- The 2026-11-15 commit messages are "." and "Add gnhf bun.lock and drop treehouse.toml"; the first one carries the large deletion without explanation.
- Four untitled multi-megabyte images sit at the root with no reference.
- The vendored projects have no recorded source revision. Commit `3bd0003` (2026-10-24) is titled "remove inspiration", yet `inspiration/` is present at HEAD.
- Not determined: which parts of `references/` differ from upstream Nelson beyond the script placeholders, and what the images are for.
