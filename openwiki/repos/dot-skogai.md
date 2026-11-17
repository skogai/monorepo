---
type: repository
title: dot-skogai
description: Older shared SkogAI agent workspace (routers, knowledge store, memory, docs library, journal, research projects). Quiet since 2026-09-27 and mid-migration; its argc toolchain has left the tree and its scripts and skills are symlinks to the owner's workstation.
tags: [workspace, archive, knowledge, journal, routers, migration]
repo: skogai/dot-skogai
commit: 973dc2a
last_commit: 2026-09-27
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/dot-skogai/SKOGAI.md
  - repos/dot-skogai/CLAUDE.md
  - repos/dot-skogai/INDEX.md
  - repos/dot-skogai/mise.toml
  - repos/dot-skogai/gptme.toml
  - repos/dot-skogai/.envrc
  - repos/dot-skogai/.mcp.json
  - repos/dot-skogai/.openwikiignore
  - repos/dot-skogai/.github/workflows/openwiki-update.yml
  - repos/dot-skogai/.claude/commands/hi.md
  - repos/dot-skogai/knowledge/DECISIONS.md
  - repos/dot-skogai/plans/dot-skogai/migration-plan.md
  - repos/dot-skogai/docs/SKOGAI.md
  - repos/dot-skogai/projects/SKOGAI.md
  - repos/dot-skogai/openwiki/quickstart.md
  - repos/dot-skogai/openwiki/testing/verification-and-drift.md
  - repos/dot-skogai/openwiki/.last-update.json
---

# dot-skogai

**`dot-skogai` is the older shared SkogAI agent workspace: the `.skogai/` folder that other repos consumed, holding routers, a knowledge store, working memory, a docs library, a journal and small research projects.** It once also held an argc tool and agent toolchain. A migration planned in July 2026 moved that toolchain out, but the root router and `mise.toml` still describe it. State: quiet archive. The last commit is 2026-09-27, 53 of the 71 visible commits are from July 2026, and nothing in the tree can be run from a fresh clone.

This page is a map at overview depth, built from listings, routers and sampling. The repo has its own generated wiki in `openwiki/` (see below), which was used for navigation and checked against the tree.

## Source map

Counts are tracked files. 225 of the 623 tracked files are symlinks.

| Path | Files | Holds |
|---|---|---|
| `SKOGAI.md` | 1 | The root router and single entry point. `AGENTS.md` is a symlink to it; `CLAUDE.md` `@`-links it. |
| `scripts/` | 122 | 121 symlinks into `~/.local/src/skills/extras/scripts/`. Names only: `context/` (25), `github/` (10), `git-hooks/` (10), `sandbox/` (8), `linear/` (7), `precommit/` (6), worktree hooks, lesson MCP servers, search and fetch helpers. |
| `skills/` | 101 | 100 symlinks into `~/.local/src/skills/skills/` plus `.skillshare-manifest.json`. Names include `skogai-routing`, `skogai-jq`, `skogai-argc`, `skogai-prompting`, `skogai-librarian`, the `bm-*` and `memory-*` families, `paseo-*`, `ponytail-*`. |
| `journal/` | 114 | Dated folders `YYYY-MM-DD/` with one or more entries each, plus `CONVENTIONS.md`. Folder dates run 2025-03-15 to 2026-09. Busiest: 2025-06 (27 entries), 2026-02 (27, of which 21 on one day), 2026-03 (16). |
| `docs/` | 92 | Reference library. `claude-code/` (59, vendored upstream Claude Code docs), `skogix/` (23, owner documents and a `.story/` subfolder), `rtk/` (2), `environments/` (2), `file-structure.md`, `skogfences.md`, routers. |
| `knowledge/` | 39 | Durable store. `decisions/` (13 dated ADR-style files, 12 of them from 2026-07-21), `lessons/` (5), `patterns/style/` (11 style guides), `DECISIONS.md` index, `MEMORY.md`, two loose notes. |
| `inbox/` | 36 | `outbox/` (25) and `inbox/` (1) hold timestamped test messages from 2026-09-16. The root holds agent bootstrap files (`SOUL.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOT.md`, `TOOLS.md`, `agents.yaml`). |
| `openwiki/` | 31 | Generated wiki: 11 pages, 6 section indexes, claim files and manifests. Last updated 2026-09-26. |
| `projects/` | 24 | Research workspaces: `navigate-skogai/` (8), `skogdiff/` (4), `skogai-devcontainer/` (4), `web-setup-for-claude/` (2), `dot-skogai/` (2), `harness/` (1). |
| `memory/` | 19 | Working memory. `feedback/` (9 behaviour corrections) plus three more at the root, `references/` (3), indexes `MEMORY.md`, `GLOSSARY.md`, `PROJECTS.md`. |
| `personal/skogix/` | 16 | The owner's routing file `SKOGIX.md` and owner documents (notation, definitions, introductions, a "soul" document). |
| `people/` | 2 | Person notes. |
| `plans/dot-skogai/` | 2 | `migration-plan.md` and `module-inventory.md`. |
| `.claude/` | 7 | `settings.json`, a `/hi` command, four skills (`debug-issue`, `explore-codebase`, `refactor-safely`, `review-changes`). |
| `.codex/`, `.config/wt.toml`, `.mcp.json`, `.envrc`, `mise.toml`, `gptme.toml` | 7 | Harness configuration for Codex, worktrunk, MCP, direnv, mise and gptme. |
| `.github/workflows/` | 2 | `claude.yml` and `openwiki-update.yml`. |
| `bin/install-skogcli` | 1 | Three-line installer for `skogcli`. |
| `schemas/router.md` | 1 | The schema for router files. |
| `INDEX.md` | 1 | A CodeLore MCP project list with 26 names, all "(no description)". Half of the names are not directories here. |

## How it works

### Routers

Every directory with rules of its own has a `SKOGAI.md` router with an `AGENTS.md` symlink beside it. Routers use `@path` references inside XML-style blocks. The root router has blocks for routes (`SKOGAI.md:10`), modules (`:45`), knowledge (`:73`), memory (`:126`), hooks (`:136`), conventions (`:159`), rules (`:172`) and commands (`:182`). All-caps files such as `DECISIONS.md` and `MEMORY.md` are indexes with one line per entry.

### Stores

| Store | Location | Rule the router gives |
|---|---|---|
| Decisions | `knowledge/decisions/` | ADR style, date-prefixed file names. |
| Lessons | `knowledge/lessons/` | YAML frontmatter with `match.keywords`, so a matcher can inject them by keyword. |
| Patterns | `knowledge/patterns/` | Timeless, no date prefix. |
| Memory | `memory/` | Short-lived working context, updated often. |
| Journal | `journal/` | Dated first-person entries. |

The matcher itself (`lesson_matcher.py`) is described in the root router but is not in the tree.

### The migration

`plans/dot-skogai/module-inventory.md` lists the modules the repo held and `plans/dot-skogai/migration-plan.md` orders their removal in seven stages, 0 to 6 (`migration-plan.md:44-129`). Each module has a decision file dated 2026-07-21 under `knowledge/decisions/`. The plan names these destinations:

- `skogai/tools` for `tools/`, `agents/`, the MCP bridge and the MCP llm-functions server.
- `skogai/skoghooks` for the lesson matcher engine.
- `skogai/skogai` for `projects/*`.
- Destinations for `skogai-jq`, `skogai-workflow`, `dot-core` and per-repo data were left open.

At HEAD, `Argcfile.sh`, `argc/`, `agents/`, `tools/`, `templates/` and `config/` are absent, so the removal side of the plan has happened. Whether each module arrived at its destination was not checked here.

### What is worth mining

- **Decisions.** `knowledge/DECISIONS.md` (two dated blocks: the January 2026 design choices for argc, `@` notation and submodule distribution; the April 2026 settings portability rules) and the 13 files in `knowledge/decisions/`.
- **Style and conventions.** `knowledge/patterns/style/` (naming, commit conventions, `@` references, XML conventions, context engineering, anti-patterns) and `schemas/router.md`.
- **Agent feedback.** `memory/feedback/` and the `memory/feedback_*.md` files record corrections to agent behaviour, one rule per file.
- **Dated record.** `journal/` is the longest-running material in the repo and predates the git history by more than a year.
- **Owner documents.** `personal/skogix/` and `docs/skogix/` (notation, definitions, introductions).
- **Agent identity files.** `inbox/SOUL.md`, `IDENTITY.md`, `USER.md` and siblings.
- **Cross-repo navigation notes.** `projects/navigate-skogai/` has reference files on `dash-skogai` and `dot-skogai` and two write-ups on understanding a repo from diffs.
- **Environment research.** `projects/web-setup-for-claude/`, `projects/skogai-devcontainer/`, `docs/environments/`.

### The repo's own `openwiki/`

Generated by OpenWiki 0.5.2 with the `init` command, last updated 2026-09-26 at commit `8579dd2` (`openwiki/.last-update.json`). The scheduled workflow `.github/workflows/openwiki-update.yml` is set to refresh it daily. Pages: `quickstart.md`, `architecture/{overview,routing-and-conventions}.md`, `concepts/{docs-library,hooks-and-context-injection,knowledge-and-memory}.md`, `operations/{harness-configuration,shared-scripts-and-skills}.md`, `projects/research-projects.md`, `testing/verification-and-drift.md`, `workflows/migration-plan.md`.

`.openwikiignore` excludes `journal/`, `personal/`, `people/`, `inbox/outbox/`, `inbox/inbox/` and `docs/claude-code/`, so that wiki does not cover the personal material or the journal. Its drift inventory was spot-checked against the tree and holds: the missing files it lists are missing. It is two commits behind HEAD; those commits add journal entries and a "WIP" change.

### Date range

The clone is shallow: 71 commits visible, 2026-07-11 to 2026-09-27. The monorepo survey records 403 commits in total. Journal folder dates start at 2025-03-15, and the oldest decision file is dated 2026-01-20.

## How to use it

Reading works anywhere. Running does not.

- **`mise.toml`** defines tasks `setup` (alias `init`), `build`, `check`, `test` and `clean` (`mise.toml:16-41`). All wrap `argc` commands that need `Argcfile.sh`, `tools/`, `agents/` and `argc/`, which are absent.
- **Root router commands** (`SKOGAI.md:182`): `argc check`, `argc build`, `argc test`, `argc run@tool`, `argc run@agent`, `argc mcp check`. Same dependency, same result.
- **`scripts/` and `skills/`** resolve only where `~/.local/src/skills` exists, which is the owner's workstation. That includes `/hi`, which calls `scripts/context/context.sh`.
- **`.envrc`** activates `.venv` and evaluates `skogcli config export-env --namespace skogai,dot-skogai`. `bin/install-skogcli` installs `skogcli`.
- **`mise.toml` env** sets `SKOGAI_CONFIG` and `SKOGAI_CONFIG_DIR` to the relative path `.skogai/config` (`mise.toml:49-50`) and loads a gitignored `.env`. The comment names the expected variables: `WEB_SEARCH_MODEL`, `PERPLEXITY_API_KEY`, `TAVILY_API_KEY`, `WOLFRAM_API_ID`, `TWILIO_*`, `EMAIL_SMTP_ADDR`, `USQL_DSN`.
- **`.mcp.json`** registers `code-review-graph` (with a hard-coded `cwd` in the owner's home directory) and `skogai-think` (the sequential-thinking server).
- **Consumer model.** A consuming repo sees this repo as `.skogai/`, originally by git submodule on a per-project branch and later by symlink (`knowledge/DECISIONS.md`). Inside this repo `.skogai` is meant to point at `.`; that link is gitignored and not in the clone.

## Relations to other SkogAI repos

- **`skogai/tools`, `skogai/skoghooks`, `skogai/skogai`**: named migration destinations (above). `openwiki/quickstart.md` stresses that this repo is different from `skogai/skogai`.
- **`skogai2-dot-skogai`**: the monorepo survey describes it as a minimal restart of the same concept (three files, 2026-11-01). Nothing in this repo refers to it.
- **`dash-skogai`**: `projects/navigate-skogai/navigate-skogai/references/dash-skogai.md` documents it alongside this repo.
- **`docs`**: `docs/skogix/` and `personal/skogix/` here carry the same owner documents as `skogix/` in the `docs` repo. `notation.md` and `keymapping.md` are byte-identical across the repos; `claude-soul.md`, `definitions.md`, `introduction.md` and `a-portrait-in-nine-chapters.md` differ. Neither repo says which copy is current.
- **Shared skills checkout**: all of `skills/` and `scripts/` point at `~/.local/src/skills`, a separate checkout managed with skillshare. Which catalog repo that is could not be determined from this tree.
- **`skogai-jq`, `skogai-workflow`, `skogai-lessons`, `dot-core`**: described as modules in the root router (`SKOGAI.md:45`) and scheduled to ship as plugins or skills.
- **External tools**: argc, aichat and llm-functions, gptme and gptme-contrib, `gptodo`, `skogcli`, worktrunk (`.config/wt.toml`), RTK, Basic Memory, Linear, Codex.
- **Environment variables** in tracked files: `SKOGAI_ROOT` (most frequent), `SKOGAI_CONFIG`, `SKOGAI_CONFIG_DIR`, `SKOGAI_MODE`, `SKOGAI_DOCS`, `SKOGAI_TEMP`, and single mentions of `SKOGAI_TEMPLATES_DIR`, `SKOGAI_SRC`, `SKOGAI_SCRIPTS_DIR`, `SKOGAI_PERSONA_HOME`, `SKOGAI_LLM_FUNCTIONS_PATH`, `SKOGAI_LLM_BASE_URL`.

## Gaps and stale references

- **Root router names absent files**: `@SKOGIX.md` (the file is at `personal/skogix/SKOGIX.md`), `@agents/SKOGAI.md`, `./references/`, `@templates/`, `@knowledge/lessons/CLAUDE.md`, `@memory/CLAUDE.md`, and the whole file tree at `SKOGAI.md:28` (`Argcfile.sh`, `argc/`, `agents/`, `tools/`, `tools.txt`, `agents.txt`). It lists `@knowledge/SKOGAI.md` and `@memory/SKOGAI.md` twice.
- **`scripts/SKOGAI.md`** is tracked but is a dangling symlink off the owner's machine. The root rule "do not hardcode `/home/skogix/...`" is contradicted by 221 absolute symlinks and by `.mcp.json`.
- **`gptme.toml`** injects `README.md`, `ARCHITECTURE.md`, `ABOUT.md`, `SOUL.md`, `TASKS.md`, `TOOLS.md`, `lessons/README.md` and `projects/README.md` and runs `scripts/context.sh` (`gptme.toml:5-17`). None exist at those paths; `SOUL.md` and `TOOLS.md` exist only under `inbox/`.
- **`docs/SKOGAI.md`** routes `@fetch-docs.sh`, which is absent, so the vendored `docs/claude-code/` cannot be refreshed from here.
- **`projects/SKOGAI.md`** routes `aws-agent-toolkit/SKOGAI.md`; commit `016e8df` (2026-08-25) removed that project.
- **`INDEX.md`** lists 26 CodeLore projects with no descriptions, including directories that do not exist (`agents`, `argc`, `config`, `messages`, `plugins`, `templates`, `tools`, `utils`).
- **No tests or CI for content.** The root router says so itself (`SKOGAI.md:195`).
- **Personal material.** `journal/`, `personal/`, `people/` and `inbox/` are first-person or about named people. Treat the repo as private.
- **Two commit messages** (`d2fc633`, `dfa5a2b`, 2026-07-23) are stray model output, not descriptions of a change.
- **Not determined:** whether the migrated modules exist at their destinations, whether the daily OpenWiki workflow still runs (its last recorded update is 2026-09-26), the history before the shallow boundary, and the content behind the symlinked scripts and skills.
