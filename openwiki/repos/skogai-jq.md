---
type: repository
title: skogai-jq
description: A Claude Code / Codex skill holding 70 schema-described jq transforms, each with its own test script and fixtures. Declared the canonical copy on 2026-11-14; otherwise unchanged since its single import commit.
tags: [jq, skill, json, transforms, claude-code]
repo: skogai/skogai-jq
commit: a8ed413
last_commit: 2026-11-14
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai-jq/AGENTS.md
  - repos/skogai-jq/SKILL.md
  - repos/skogai-jq/README.md
  - repos/skogai-jq/CLAUDE.md
  - repos/skogai-jq/test-all.sh
  - repos/skogai-jq/agents/openai.yaml
  - repos/skogai-jq/crud-get/transform.jq
  - repos/skogai-jq/crud-get/schema.json
  - repos/skogai-jq/crud-get/test.sh
  - repos/skogai-jq/scripts/claude-stream.jq
  - repos/skogai-jq/scripts/claude-to-skogchat.sh
  - repos/skogai-jq/backlog.md
  - repos/skogai-jq/whats-next.md
  - repos/skogai-jq/tasks/h-implement-crud-delete.md
---

# skogai-jq

**A reusable agent skill that packages 70 small jq transforms, each in its own directory with a schema, a test script and fixtures.** An agent picks a transform by reading its `schema.json` and runs it directly with `jq -f`. The repo has two commits: an import on 2026-06-03 and a docs-only change on 2026-11-14 (PR #1) that declares this repo the source of truth and retires the copy in skogai-core. It is stable and quiet rather than under development: the planning files inside it date from late 2025.

## Source map

The repo has 1,105 tracked files in 76 top-level directories. 70 of the directories are transforms.

| Path | Holds |
|---|---|
| `SKILL.md` | Skill entry point (`name: skogai-jq`): categories, invocation pattern, pointers |
| `AGENTS.md` | Structure, conventions, anti-patterns, commands, source-of-truth note |
| `CLAUDE.md` | Working rules and jq pitfalls (227 lines) |
| `README.md` | Install as a skill, philosophy, per-transform usage |
| `IMPLEMENTATION_SPEC.md` | The contract a transform must follow (636 lines) |
| `CHEAT_SHEET.md`, `USAGE_EXAMPLES.md` | Lookup table of transforms and worked examples |
| `references/` | Byte-identical copies of `CHEAT_SHEET.md`, `IMPLEMENTATION_SPEC.md`, `USAGE_EXAMPLES.md`, `README.md` |
| `test-all.sh` | Runs every `*/test.sh` and prints a pass/fail summary |
| `<transform>/` | `transform.jq`, `schema.json`, `test.sh`, `test-input-*.json` |
| `scripts/claude-stream.jq` | Turns `claude --output-format stream-json` output into readable progress lines |
| `scripts/claude-to-skogchat.sh` | Converts Claude Code JSONL history to "skogchat" format |
| `schemas/` | 16 JSON Schemas: `transform`, `message`, `skogchat-message`, plus document-type schemas |
| `schema-fixtures/` | 5 fixture files (`index.json` and four named after transforms) |
| `agents/openai.yaml` | Codex interface metadata: display name "SkogAI JQ" |
| `tasks/` | 60 planning tickets (`h-implement-*`, `m-implement-*`), not runtime code |
| `backlog.md`, `proposals.md`, `patterns.md`, `vision.md`, `examples.md`, `whats-next.md` | Planning and design notes |

## How it works

### The transform contract

Every transform directory has all of `transform.jq`, `schema.json` and `test.sh` (checked: 70 of each). There is no wrapper and no shared library. A transform is one jq program, and its parameters arrive through `--arg` or `--argjson`:

```bash
jq -f <transform-dir>/transform.jq [--arg key val] [--argjson key json] input.json
```

`schema.json` describes the transform for the agent. In `crud-get/schema.json` the fields are `name`, `description`, `version` (`1.0.0`), `input`, `args` (each with `type`, `required`, `description`), `output`, `examples` and `tags`. The directory name and the schema `name` must match (`AGENTS.md:31`).

`test.sh` is standalone Bash with `set -euo pipefail`. It resolves its own directory, runs the transform against numbered fixtures, compares exact output strings and prints `PASS` or `FAIL` per case (`crud-get/test.sh:1-22`). `test-all.sh:16-30` discovers the scripts by glob, so a new transform needs no registration.

Transforms compose through pipes: the output of one `jq -f` call is the input of the next (`SKILL.md`, "Compose multiple transforms").

### Inventory by family

| Family | Transforms |
|---|---|
| CRUD on paths | `crud-get`, `crud-set`, `crud-delete`, `crud-has`, `crud-merge`, `crud-query` |
| Arrays | `array-append`, `array-chunk`, `array-filter`, `array-flatten`, `array-map`, `array-prepend`, `array-reduce`, `array-unique` |
| Strings | `string-join`, `string-match`, `string-replace`, `string-split`, `string-trim`, `string-truncate`, `collapse-newlines` |
| Fields | `add-field`, `copy-field`, `remove-field`, `rename-field`, `pick-fields`, `has-field` |
| Extraction | `extract-code-blocks`, `extract-content-array`, `extract-first-line`, `extract-mentions`, `extract-role-content`, `extract-tool-calls`, `extract-urls` |
| Filtering, grouping, stats | `filter-by-date-range`, `filter-by-pattern`, `filter-by-role`, `filter-by-type`, `group-by-field`, `sort-by-field`, `count-by-field`, `deduplicate-by-content`, `generate-stats` |
| Predicates | `has-code-block`, `has-url`, `is-empty-string`, `is-timestamp`, `is-uuid` |
| Validation | `validate-format`, `validate-message-schema`, `validate-range`, `validate-required`, `validate-types`, `schema-validation` |
| Type conversion | `to-array`, `to-boolean`, `to-number`, `to-object`, `to-string` |
| Chat messages | `format-message`, `format-timestamp`, `normalize-timestamp`, `generate-message-id`, `summarize-tool-call`, `join-todos`, `to-skogchat` |
| Composition and tooling | `pipe`, `map-transform`, `try-transform`, `test-generator` |

Many transforms target chat-message JSON (roles, tool calls, timestamps), which matches the two helper scripts under `scripts/`.

### Rules the repo sets for transform authors

`AGENTS.md:38-45` lists the anti-patterns: no `// fallback` where `null` or `false` are valid values, no `getpath(...) != null` as an existence test, check the input type before `map()`, never hard-code arguments, and no wrappers around the direct jq call.

I read only `crud-get` in full. The other 69 transforms, their fixtures and the long reference documents were not read.

## How to use it

- Prerequisites: Bash and jq 1.6 or later. The README says the consolidation tests used jq 1.8.2.
- Install as a skill: clone or symlink the whole checkout into the harness's skill directory under the name `skogai-jq`. The README's example targets Codex (`~/.codex/skills/skogai-jq`). The README states that live harness discovery and installation have not been tested.
- Resolve paths relative to the directory that holds `SKILL.md`, not the working directory, and use an absolute path with `jq -f` (`SKILL.md:90-96`).
- Find a transform through the categories in `SKILL.md`, then `references/CHEAT_SHEET.md`, then the transform's `schema.json`.
- Tests: `./test-all.sh` for everything, `./<transform>/test.sh` for one.
- Adding a transform: follow `IMPLEMENTATION_SPEC.md`.

## Relations to other SkogAI repos

- `skogai/skogai-core` holds a retired copy at `todo/skills/skogai-jq` (1,083 files). `README.md` and `AGENTS.md:60-63` say not to restore it and to contribute here. Compared with that copy, this repo adds `agents/`, `schemas/` and `schema-fixtures/`, and differs in `AGENTS.md`, `CLAUDE.md`, `README.md`, `SKILL.md`, `references/README.md` and `array-map/test.sh`. See [skogai-core](skogai-core.md).
- `schemas/` has 11 files with the same names as `skogai-core/skills/skogai-core/schemas/` (`decision`, `defs`, `document`, `frontmatter`, `lesson`, `list`, `pattern`, `principle`, `reference`, `router`, `script`, `template`, `workflow`). The ones compared differ in content, so the two sets have diverged.
- skogai-core's test suite and CLAUDE.md still expect a `plugins/skogai-jq/` directory with a `scripts/skogai-jq.sh` hook helper. That helper is not in this repo; a version exists at `skogai-core/todo/scripts/skogai-jq.sh`.
- The frontmatter `permalink` values (`skogai/skills/skogai-jq/...`) show the files once lived in a larger knowledge tree. Which repo that was is not stated here.
- The monorepo's cached `agents/skogai-jq.md` is this repo's `AGENTS.md`.

## Gaps and stale references

- `SKILL.md`'s heading and prose call the library `jq-transforms`, the earlier name; the frontmatter name is `skogai-jq`.
- `whats-next.md` is a session handoff dated 2025-12-06 that names a workstation path (`/home/skogix/dev/skogix/src/jq-transforms`) and commits that are not in this repo's two-commit history.
- The 60 files in `tasks/` are tickets with `status: pending` and unfilled template text (for example `# [Human-Readable Title]` in `tasks/h-implement-crud-delete.md`), although the transforms they name exist. `backlog.md` marks those items done.
- `references/` duplicates four root documents byte for byte. `AGENTS.md:57` warns against divergent edits but nothing enforces it. `references/README.md` therefore also carries the install text.
- `AGENTS.md:58` notes that docs claim 8-17 tests per transform while some harnesses are smaller.
- `crud-get/transform.jq:16` tests `$value != null`, the existence pattern that `AGENTS.md:40` lists as an anti-pattern, so a present `null` and a missing path are not distinguished there.
- Nothing in the transforms or docs that I searched references `schemas/` or `schema-fixtures/`; how they are consumed was not determined.
- There is no CI configuration and no plugin manifest (`.claude-plugin/`); the repo is a bare skill.
