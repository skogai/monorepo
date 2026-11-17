---
type: repository
title: skogai2-skogai-routing
description: A documentation-only convention (version 0.1.0) for finding agent guidance by following ownership between files, plus one installable skill. Nine files, quiet since 2026-10-31.
tags: [routing, convention, skill, documentation, agent-context]
repo: skogai2/skogai-routing
commit: 2e51d9a
last_commit: 2026-10-31
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-skogai-routing/SKOGAI.md
  - repos/skogai2-skogai-routing/docs/intentions.md
  - repos/skogai2-skogai-routing/docs/glossary.md
  - repos/skogai2-skogai-routing/docs/changelog.md
  - repos/skogai2-skogai-routing/skills/skogai-routing/SKILL.md
  - repos/skogai2-skogai-routing/skills/skogai-routing/references/dash-skogai.md
  - repos/skogai2-skogai-routing/skills/skogai-routing/references/dot-skogai.md
  - repos/skogai2-skogai-routing/skills/skogai-routing/references/skogfences.md
  - repos/skogai2-skogai-routing/.gitignore
---

# skogai2-skogai-routing

**skogai-routing is a written convention for how files declare ownership of other files, and how an agent walks that structure one step at a time to find the guidance it needs.** The repo holds no code: nine tracked files, 255 lines, all Markdown apart from `.gitignore`. It is at version 0.1.0 (`SKOGAI.md` frontmatter), whose stated scope is "the routing step only". State: quiet. The history is four commits, an init on 2026-10-09 and a compaction to a single entry point merged on 2026-10-31; nothing since.

## Source map

| Path | Holds |
|---|---|
| `SKOGAI.md` | The root routing file and single entry point. Frontmatter (`type: root`, `permalink: skogai-routing/skogai`, `version: 0.1.0`), a `<quick_start>` block and a `<routes>` block with four `@./` links. |
| `docs/intentions.md` | Why the project exists: the problem, the core intention, the ideas behind it, and how it fits with a separate knowledge layer. |
| `docs/glossary.md` | The five defined terms: `ownership`, `routing-file`, `leaf`, `root`, `ownership-(relationship)`. Each has an `_avoid_` list of words not to use. |
| `docs/changelog.md` | One entry, 0.1.0, listing what the compaction changed. |
| `skills/skogai-routing/SKILL.md` | The installable skill. Frontmatter (`name`, `description`, `permalink`) and a `<routes>` block pointing at three references. No instructions of its own. |
| `skills/skogai-routing/references/dash-skogai.md` | What `/skogai` is and why it is named "dash-skogai". |
| `skills/skogai-routing/references/dot-skogai.md` | What `.skogai` is and its history. |
| `skills/skogai-routing/references/skogfences.md` | An essay on "skogfences": giving agents their own Unix home instead of a sandbox. |
| `.gitignore` | Ignores `.skogai/logs/`, `**/hook-tap/log.jsonl` and `.skogai/journal.md`. |

## How it works

### The convention

The mechanism is defined in prose only, in `docs/glossary.md` and `docs/intentions.md`.

- A **routing file** is a file named in all-caps (`SKOGAI.md`, `CLAUDE.md`, `MEMORY.md`, ...) that owns other files and links, references or injects them. The glossary says the all-caps name is the formal marker of the type: a lowercase file doing the same job is not a routing file (`docs/glossary.md:24`).
- A **leaf** has an owner and owns nothing (`docs/glossary.md:29`).
- The **root** is the one routing file at a repo's git root (`SKOGAI.md`, `CLAUDE.md` or `AGENTS.md`). "Root" as a path is always the closest `.git` folder walking up. The root's `permalink` records the repo's external identity, not a parent (`docs/glossary.md:34`).
- **Ownership is non-transitive.** If a owns b and b owns c, a does not own c. Every lookup is exactly one hop (`docs/glossary.md:39`).

The reading procedure is stated in `SKOGAI.md:10`: start at the entry point, pick one route, take one step, stop when the task has what it needs. `docs/intentions.md` adds the design rules: the entry point routes and does not teach; one job per piece (route, procedure, fact, output shape, repeatable check); plain text first; validation as a guard rail only.

### File shape used in this repo

Each file has YAML frontmatter with `title`, `type` (`root` or `reference`) and `permalink` (`skogai-routing/<name>`). Routing files carry a `<routes>` XML-style block whose entries are `@./relative/path - one-line description`. The repo follows its own rule: only `SKOGAI.md` and `SKILL.md` are all-caps, and the changelog records moving intentions and glossary to lowercase leaves for that reason (`docs/changelog.md:14`).

### The skill

`skills/skogai-routing/SKILL.md` is a router with three routes. Its description tells an agent to use it whenever navigating SkogAI projects, documentation or configuration. The three references are background, not procedure:

- `dash-skogai.md`: `/skogai` sits directly under `/` on purpose. It is owned by one user and the group `skogai` with the setgid bit (`drwxrwsr-x`), so files created by any member (human users and agent system users) inherit the group.
- `dot-skogai.md`: `.skogai` started as `$HOME/.skogai`, joined by per-agent `$HOME/.<agent-name>` folders. It says the `SkogAI/.skogai` repository is now both the base configuration and a submodule to add to projects.
- `skogfences.md`: the argument that agents should get their own home directory, users, groups and permissions, with collaboration in explicitly shared spaces. Wrapped in a `[@skogix.concept:$skogfences]` tag.

## How to use it

There is nothing to build or run. No `mise.toml`, scripts, tests or plugin manifest are tracked.

- To read the convention: open `SKOGAI.md` and follow one route.
- To use the skill: `skills/skogai-routing/` is laid out as a Claude Code skill folder (`SKILL.md` plus `references/`). The repo does not say how to install it; there is no `.claude-plugin/` manifest or marketplace entry here.
- To apply the convention in another repo: put one all-caps routing file at the git root with frontmatter and a `<routes>` block, as `SKOGAI.md` does.

## Relations to other SkogAI repos

- **`/skogai` (dash-skogai) and `.skogai` (dot-skogai).** The skill exists to navigate these two places. The catalog has `skogai2-dash-skogai` and `skogai2-dot-skogai` repos; this repo describes the concepts, it does not depend on their files.
- **`SkogAI/.skogai`.** Named in `references/dot-skogai.md` as the base-configuration and submodule repository.
- **skogix.** Commit `8beb60d` ignores the hook-written `.skogai/journal.md` "matching skogix". The `.gitignore` entries show the repo is worked on with hooks that write `.skogai/logs/` and `.skogai/journal.md` (the skogai-core journal-and-log hook seen in other repos), and that a `hook-tap` plugin once wrote a log into the skill folder.
- **Older `skogai-routing` (skogai org).** The monorepo survey lists an older, dormant repo of the same name; this one reads as a compact restart. The changelog mentions an old `dot-skogai/…` permalink prefix, now replaced by `skogai-routing/…`.
- **Shared convention.** The `<routes>` block and `permalink` frontmatter appear in other skogai2 repos (for example the `skogai-runner` workorders file with `type: routing`, and the earlier `skogai-fleet` `AGENTS.md`).
- **Knowledge layer.** `docs/intentions.md` says a knowledge bundle could sit under the routes. No specific format or repo is named.

## Gaps and stale references

- No validation tooling. `docs/intentions.md` lists "checks as guard rails", and nothing in the repo implements a check.
- The glossary entry for `ownership` says an owner can be a "file, concept, or tag". Only file ownership is defined further.
- `docs/intentions.md` describes itself as "a starting point to correct, not a finished position".
- `SKILL.md` gives no steps for actually walking routes; the procedure lives only in `SKOGAI.md` and `docs/`, which are outside the skill folder and would not ship with it.
- `references/skogfences.md` has the frontmatter title `welcome-away-from-home` while its permalink and filename say `skogfences`.
- `references/dot-skogai.md` contains the typo "SkogaAI".
- The changelog records fixing a dangling pointer to `docs/concepts/definitions.md`; no such pointer remains at HEAD.
