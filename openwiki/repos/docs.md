---
type: repository
title: docs
description: Knowledge and history archive of the SkogAI ecosystem (agent personas, memory blocks, lore, governance records, prompts, old technical docs). Dormant and mid-consolidation; three overlapping trees and no working root index.
tags: [archive, knowledge, lore, personas, memory-blocks, governance]
repo: skogai/docs
commit: 27151f2
last_commit: 2026-10-06
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/docs/CLAUDE.md
  - repos/docs/.claude/CLAUDE.md
  - repos/docs/.mcp.json
  - repos/docs/.gitignore
  - repos/docs/SKILL-REVIEW.md
  - repos/docs/merge/README.md
  - repos/docs/merge/CLAUDE.md
  - repos/docs/merge/REPOSITORY-INDEX.md
  - repos/docs/todo/README.md
  - repos/docs/todo/CLAUDE.md
  - repos/docs/todo/docs-repository.md
  - repos/docs/skogix/SKOGAI.md
  - repos/docs/merge/governance/phases/skogai-0.2-democracy.md
---

# docs

**`docs` is a 2,536-file archive of SkogAI knowledge and history, not a maintained documentation site.** It holds agent personas and memory blocks, lore, governance records, prompt libraries, agent journals and older technical documentation, most of it Markdown (1,211 `.md`, 99 `.txt`). The content is spread over three overlapping trees (`merge/`, `todo/`, `skogix/`) left from several unfinished reorganisations, and the root `CLAUDE.md` describes a layout that no longer exists. State: dormant. The last commit is 2026-10-06, only 6 commits fall after May 2026, and many commit messages are a bare `.`.

This page is a map for finding material. It was built from file listings, router files and sampling. Individual documents were not read in full.

## Source map

Counts are tracked files (`git ls-files`).

| Path | Files | Holds |
|---|---|---|
| `merge/` | 1,925 | The largest tree. The former repo layout, moved under one directory. 954 files once the database dump is excluded. |
| `merge/media/aldervall-postgres/` | 971 | A committed PostgreSQL 17 data directory (`pgdata/`), a server log file and two Claude Code session files. Not documentation. |
| `merge/media/` (rest) | 52 | Generated images and short videos, numbered screenshots. |
| `merge/todo/` | 301 | An older snapshot of the repo nested inside itself: `curated/home/skogix/skogai/docs/` (238 files, of which 120 sit under `REAL-OUTPUT-FROM-REAL-AI/`), plus `curated/todo/` (21 memory-system guides). |
| `merge/historical/` | 122 | Archives: `archived/` (31, includes `lore-old/`), `skogai-memory/` (18), `analysis/` (17), `tracking/`, `testing/`, `planning/`, `logs/`, `notes/`, `communications/`. |
| `merge/technical/` | 121 | `memory-system/` (64, of which 42 are `memory-extraction-epistemic-framework/`), `notation/` (20), `dev/` (12), `ansible/` (11), `cloudflare/` (4). |
| `merge/agents/` | 108 | Personas and memory blocks per agent: `claude/` (37), `amy/` (19), `dot/` (14), `goose/` (14), `intern/` (1), plus `automation/` (21, a documentation-agent system with Python scripts and hook logs). |
| `merge/lore/` | 100 | `skogix/` (58, of which `blocks/` holds 44 concept blocks), `important-moments/` (9), `origin/` (8), `philosophy/` (6), `meta/` (6), `events/`, `personas/`. |
| `merge/prompts/` | 88 | `old/` (36), `aichat/` (32), `topics/` (7), `agents/` (2), and loose role prompts. |
| `merge/skogai/` | 20 | Ecosystem overview, philosophy, notation foundations, agent roles, tool notes. |
| `merge/governance/`, `merge/principles/`, `merge/mcp/`, `merge/claude/`, `merge/reference/`, `merge/personas/`, `merge/architecture/`, `merge/_workspace/`, `merge/people/`, `merge/workflows/` | 7, 6, 7, 6, 4, 2, 2, 3, 1, 1 | Small sets: library sessions and phase declarations; design principles; MCP server notes; session handovers; notation v1 and v2 specs; two persona files. |
| `merge/README.md`, `merge/CLAUDE.md`, `merge/REPOSITORY-INDEX.md` | 3 | The old root README, the old 488-line agent guide and an 844-line file-by-file inventory. All describe paths as if `merge/` were the repo root. |
| `todo/` | 386 | A second, differently organised docs tree (was `.todo/` until 2026-05-09). |
| `todo/agents/` | 146 | `claude/` (117: `journal/` 94, `memory-blocks/` 12, `core/` 8, a profile and a soul document), `dot/` (15), `goose/` (14). |
| `todo/interfaces/` | 83 | `goose/memory/` (74: `old/` 60, `current/` 10, three recipe YAML files), `aichat/` (8). A misspelled sibling `todo/intefaces/aichat/` holds 9 more. |
| `todo/tools/`, `todo/help/`, `todo/system/`, `todo/git/` | 33, 12, 7, 3 | Tool documentation (`argc/`, `gh/`, aichat/llm-functions guides), captured `--help` output, workstation setup notes, git-flow and submodule notes. |
| `todo/prompts/`, `todo/persona/` | 28, 15 | Lore and persona analysis prompts; character-card and lorebook guides. |
| `todo/work-orders/`, `todo/github-issues/` | 10, 12 | Work orders WO-01 to WO-10 for the skill consolidation in `SKILL-REVIEW.md`, and the same as issue drafts with a push script. |
| `todo/governance/`, `todo/memory/`, `todo/skogai/`, `todo/lore/`, `todo/context/` | 7, 11, 3, 2, 2 | Governance copies; Basic Memory notes and a committed `memory.db` (about 500 KB); two early-history documents; one dated lore entry. |
| `skogix/` | 104 | The owner's own material: notation, definitions, a "soul" document, introductions, and persona material. Most recently edited tree. |
| `skogix/.memory-blocks/` | 60 | `blocks/` (44 concept blocks), a profile, persona, notation files and seven numbered story files. |
| `skogix/WIP/` | 18 | Overviews of the ecosystem, context engineering and progressive disclosure; `skogix/` with 11 numbered memory blocks, definitions and a user profile. |
| `skogix/skogix-2/` | 13 | A later pass (2026-09-16): `SOUL.md`, notation trio, definitions, five story files. |
| `media/` | 115 | 62 `.mp4`, 48 `.png`, 5 `.jpg`. Generated media, 162 MB on disk. |
| `guides/` | 1 | A Basic Memory development-environment cheat sheet. |
| `SKILL-REVIEW.md` | 1 | Audit of 20 skills with a consolidation plan (see below). |
| `CLAUDE.md`, `.claude/CLAUDE.md`, `.mcp.json` | 3 | Root router, Repowise-generated guidance, Repowise MCP server config. |

## How it works

There is no build, pipeline or code path. The repo is read through its router files, and those disagree with the tree.

### Three trees, three generations

- **`merge/`** is the earlier canonical layout. `merge/README.md` describes `agents/`, `governance/`, `historical/`, `lore/`, `prompts/`, `skogai/`, `technical/` and `_workspace/` as top-level directories, and all eight exist under `merge/`. The commits `1201d7b` "pre-merge" and `8f4c7a4` ".todo -> todo" (both 2026-05-09) are where the trees took their present names.
- **`todo/`** describes itself as a "Production Ready (v1.0)" documentation hub (`todo/README.md:12`) with sections `context/`, `git/`, `interfaces/`, `tools/`, `system/` and others. It is tool-and-interface documentation plus the Claude agent journal.
- **`skogix/`** is routed by `skogix/SKOGAI.md` and holds the owner-authored material. It received the last content commits (2026-09-14 to 2026-10-06).

### Which copy is authoritative

No file declares this. What the tree shows:

| Material | Copies | Evidence |
|---|---|---|
| Owner notation, definitions, soul document | `skogix/*.md`, `skogix/skogix-2/`, `skogix/.memory-blocks/`, `merge/lore/skogix/` | `skogix/` root files and `skogix-2/` are newest (September 2026). Three files are byte-identical between `skogix/` and `skogix-2/`. 41 files are byte-identical between `merge/lore/skogix/` and `skogix/.memory-blocks/`. |
| Claude persona and memory blocks | `merge/agents/claude/`, `todo/agents/claude/` | Same file names, different content. The `todo/` profile has richer tags and an `agents/claude/profile` permalink. `todo/` also holds the journal and `core/`. `merge/` also holds `prompts/` and `memory/`. Neither is a superset. |
| Amy persona | `merge/agents/amy/` only (plus `merge/personas/`) | No `todo/` copy. |
| Dot and Goose | `merge/agents/{dot,goose}/` (memory blocks, profiles), `todo/agents/{dot,goose}/` | Both exist; not compared. |
| Governance | `merge/governance/`, `todo/governance/` | Same seven file names; bodies are identical apart from frontmatter in the one file compared. |
| Old repo snapshots | `merge/todo/curated/home/...` | Strictly older nested copies, including a nested copy of itself. Lowest priority. |

Working rule for a reader: start in `skogix/` for the owner's current voice and notation, `merge/agents/` and `merge/lore/` for personas and lore, `todo/agents/claude/journal/` for the dated record, and treat `merge/todo/` and `merge/historical/` as archive.

### What is worth mining

- **Personas and memory blocks.** `merge/agents/<agent>/memory-blocks/` (12 to 14 numbered blocks per agent, named by era), `merge/agents/<agent>/profile.md`, `todo/agents/claude/soul-document.md`, `skogix/WIP/skogix/memory-blocks/` (blocks 00 to 10).
- **Concept blocks.** `skogix/.memory-blocks/blocks/` (44 short named concepts such as constraint-as-feature, context minimalism, gateway architecture).
- **Notation.** `merge/reference/notation/` (v1 and v2 specs), `merge/technical/notation/` (20 files), `merge/skogai/notation/`, `skogix/notation.md` (473 lines) with a rebuttal and a poetry variant.
- **Governance and decisions.** `merge/governance/phases/` (phase declarations 0.1 "dictator", 0.2 "democracy", 0.3 index), `merge/governance/library-sessions/` (four sessions), `merge/lore/first-executive-order.md`, `merge/_workspace/drafts/`.
- **Lore.** `merge/lore/origin/`, `important-moments/`, `philosophy/`, `events/`; `merge/historical/archived/lore-old/` for the earliest material.
- **Principles.** `merge/principles/` (six short essays on context control, forking and summary precision), `merge/skogai/philosophy/`.
- **Dated record.** `todo/agents/claude/journal/` (94 entries; file names carry dates from 2025-03 onward), `merge/claude/sessions/` (handovers).
- **Prompts.** `merge/prompts/aichat/` and `merge/prompts/old/`; `todo/prompts/lore/` and `todo/prompts/personas/`.
- **Skill audit.** `SKILL-REVIEW.md` records that several skills were byte-for-byte duplicates and lays out four phases of work orders (`SKILL-REVIEW.md:64-86`); commits `1f95f09` and `1f407f2` (2026-03-18) report phases 1 and 2 done.

### Date range

The clone is shallow (68 commits visible, 2025-12-31 to 2026-10-06, busiest in March 2026 with 25). The content is older than the history: dates in file names run from 2025-02 to 2026-03, with a cluster in 2025-06, and one governance file is dated 2025-06-09. Six file names carry 2023-06 dates. Full history depth could not be determined from this clone.

## How to use it

- Read-only browsing. There are no tasks, scripts to run or install steps at the root.
- `.mcp.json` registers a `repowise` MCP server pointed at a hard-coded absolute path under the owner's home directory. `.claude/CLAUDE.md` is Repowise output, last indexed 2026-05-29 at commit `805cb8f`; `.repowise/` itself is gitignored.
- `CLAUDE.md:2-3` gives the expected location as `$SKOGAI/docs/` and the variable `SKOGAI_DOCS`.
- `todo/github-issues/push-issues.sh` and the scripts under `merge/agents/automation/documentation/` exist but were not read or run.
- Many files carry Basic Memory frontmatter (`title`, `type: note`, `permalink`); commits `bd4e84b` and `ba01b9f` added it in bulk. The permalinks encode the tree (`skogai/docs-merge-todo/...`, `skogai/todo/...`).

## Relations to other SkogAI repos

- **`dot-skogai`**: its `docs/skogix/` carries the same owner documents as this repo's `skogix/`. `notation.md` and `keymapping.md` are byte-identical across the two repos; `claude-soul.md`, `definitions.md`, `introduction.md` and `a-portrait-in-nine-chapters.md` differ. Its `journal/` covers the same period as `todo/agents/claude/journal/`.
- **Skills repos**: `SKILL-REVIEW.md` and `todo/work-orders/` audit skills named `skogai-routing`, `skogai-prompting`, `skogai-skills`, `skogai-jq`, `skogai-docs`, `nelson` and others, and name `skogai-routing` as the hub. The skills themselves are not in this repo. Commit history shows a `skogai-jq` directory added and removed in February 2026.
- **Submodule role**: `merge/CLAUDE.md` says the repo was a git submodule of a parent SkogAI workspace under the owner's home directory. Commits on 2026-04-15 and 2026-04-17 removed a `dagu` and a `memory` submodule from this repo.
- **Environment variables** named in the content: `SKOGAI_DOCS`, `SKOGAI_HOME` (most frequent), `SKOGAI_DIR`, `SKOGAI_ARGC`, `SKOGAI_PROMPT`.
- **External tools** the content documents: Basic Memory, aichat and llm-functions, argc, goose, gh, uv, Letta.

## Gaps and stale references

- **Root `CLAUDE.md` routes are broken.** It links `@agents/`, `@.docgen/`, `@lore/README` and `@tools/` (`CLAUDE.md:12-16`). None exist at the root. `agents/` and `lore/` are under `merge/`, tool docs under `todo/tools/`, and `.docgen/` is absent (only its `__pycache__` appears in `.gitignore`). Only `@skogix/` resolves.
- **`skogix/SKOGAI.md` routes `@user.md`**, which exists only at `skogix/WIP/skogix/user.md`.
- **`merge/README.md`, `merge/CLAUDE.md` and `merge/REPOSITORY-INDEX.md`** use root-relative paths that are now one level down, and the index lists directories (`.aichat-sessions/`, `.github/workflows/`, session data) that are not in the tree.
- **A database is committed.** `merge/media/aldervall-postgres/pgdata/` is a live-format PostgreSQL data directory with configuration files and write-ahead log. Its contents were not inspected. It should be reviewed for sensitive data before the repo is shared more widely. The same applies to `todo/memory/.basic-memory/memory.db` and the session files under `merge/media/aldervall-postgres/.claude/`.
- **Personal material.** Persona, profile and journal files describe a real person and private conversations. Treat the repo as private.
- **Duplicate and typo directories.** `todo/interfaces/` and `todo/intefaces/`; `merge/lore/origin/` and `merge/lore/origins`; `merge/technical/patterns` and `merge/technical/work:patterns`; nine `.bak` files; six `.md-fit` files.
- **Size.** 447 MB on disk; `media/` is 162 MB and `merge/` 63 MB. Three media files are duplicated between `media/` and `merge/media/`.
- **No consolidation plan in the tree.** Commit `a5b9414` (2026-01-09) mentions ROADMAP and STATE documents; neither exists at HEAD.
- **Not determined:** which tree the owner regards as canonical, full history before the shallow boundary, and the content of the binary and database files.
