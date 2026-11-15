---
type: repository
title: skogai-core
description: Older Claude Code plugin marketplace (`core`) built around the skogai-routing skill and its JSON schemas, with a small test plugin and a large `todo/` tree of unmigrated material. Quiet since 2026-09-11, with an unfinished migration.
tags: [claude-code, plugin-marketplace, skills, routing, json-schema, migration]
repo: skogai/skogai-core
commit: 5dfb6c1
last_commit: 2026-09-11
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai-core/.claude-plugin/marketplace.json
  - repos/skogai-core/CLAUDE.md
  - repos/skogai-core/skills/skogai-core/SKILL.md
  - repos/skogai-core/skills/skogai-core/SKOGAI.md
  - repos/skogai-core/skills/skogai-core/schemas/README.md
  - repos/skogai-core/skills/skogai-core/scripts/validate-schema.sh
  - repos/skogai-core/skills/skogai-core/scripts/_validate_file.py
  - repos/skogai-core/skills/skogai-core/scripts/create-gh-issue.sh
  - repos/skogai-core/skills/skogai-hook-debugging/SKILL.md
  - repos/skogai-core/agents/schema-converter.md
  - repos/skogai-core/scripts/claude-code-documentation.sh
  - repos/skogai-core/tests/.claude-plugin/plugin.json
  - repos/skogai-core/tests/AGENTS.md
  - repos/skogai-core/tests/README.md
  - repos/skogai-core/tests/commands/run-tests.md
  - repos/skogai-core/tests/skogai-hooks/log-event.bats
  - repos/skogai-core/tests/skogai-jq/skogai-jq.bats
  - repos/skogai-core/tests/test-helper.bash
  - repos/skogai-core/todo/.codex-plugin/plugin.json
  - repos/skogai-core/todo/AGENTS.md
  - repos/skogai-core/todo/hooks.json
  - repos/skogai-core/todo2/SKILL.md
---

# skogai-core

**A Claude Code plugin marketplace named `core` that publishes two plugins: `skogai-core`, a routing skill with JSON schemas for typed Markdown, and `skogai-tests`, a Bats testing plugin.** The live part is small (about 60 files). 1,153 of the 1,219 tracked files sit under `todo/`, an older Codex plugin called `dot-core` that is kept as migration input, and 1,083 of those are a retired copy of the jq transform library. The repo is quiet: the last commits are three merges on 2026-09-11, and before that 2026-07-30 ("remove old hooks"). The migration it describes is unfinished, and its own guidance points at a `plugins/` directory that does not exist.

Do not confuse this repo with the plugin `skogai-core` in [skogai2-marketplace](skogai2-marketplace.md). That one is a hook runtime at version 0.10.0 and shares no code with this repo.

## Source map

| Path | Holds |
|---|---|
| `.claude-plugin/marketplace.json` | Marketplace `core`: two plugin entries with inline manifests (`strict: false`) |
| `CLAUDE.md` | Repository guidelines. `AGENT.md` (singular) is a symlink to it |
| `skills/skogai-core/` | The routing skill (44 files): `SKILL.md`, `workflows/`, `references/`, `templates/`, `schemas/`, `scripts/` |
| `skills/skogai-core/SKOGAI.md` | Short local router; `AGENTS.md` and `CLAUDE.md` in that directory are symlinks to it |
| `skills/skogai-hook-debugging/SKILL.md` | Guide to Claude Code hook events and debugging (skill name `hook-debugger`) |
| `agents/schema-converter.md` | Agent that rewrites legacy Markdown into schema-valid typed documents |
| `scripts/claude-code-documentation.sh` | Downloads about 60 Claude Code docs pages with `curl` into `./tmp/docs/claude-code` |
| `tests/` | The `skogai-tests` plugin: `plugin.json`, a skill, the `/run-tests` command, two Bats suites, `test-helper.bash`, `TESTING.md` |
| `todo/` | `dot-core` Codex plugin 0.0.4: 22 hook files, 12 commands, 2 agents, 8 scripts, 11 test files, `skills/` |
| `todo/skills/skogai-jq/` | Retired copy of the jq library (1,083 files) |
| `todo/skills/skogai-gita/` | Skill for the `gita` multi-repo CLI, with CSV config |
| `todo2/` | An earlier `skogai-core` SKILL.md about marketplace management, plus older copies of the validation scripts |

## How it works

### Plugin and skill inventory

From `.claude-plugin/marketplace.json` (`metadata.pluginRoot` is `./`):

| Plugin | Version | Source | Contents |
|---|---|---|---|
| `skogai-core` | 0.0.2 | `./` (the repo root) | Skills `./skills/skogai-core` and `./skills/skogai-hook-debugging`; agent `./agents/schema-converter.md` |
| `skogai-tests` | 0.0.2 | `./tests` | Skill `skogai-tests`, command `/run-tests`, Bats suites |

Not published, but present:

| Item | Version | Where | What it is |
|---|---|---|---|
| `dot-core` | 0.0.4 | `todo/.codex-plugin/plugin.json` | Codex plugin manifest pointing at `./skills/`, `./hooks.json`, `./.mcp.json`, `./.app.json` (the last two are empty) |
| `skogai-jq` | n/a | `todo/skills/skogai-jq/` | Retired; see [skogai-jq](skogai-jq.md) |
| `skogai-gita` | n/a | `todo/skills/skogai-gita/` | gita multi-repo management skill |
| `skogai-core` (old) | n/a | `todo2/SKILL.md` | Marketplace-management skill: add the marketplace, install and update plugins |

### The routing skill

The skill directory is named `skogai-core` but its frontmatter name is `skogai-routing` (`skills/skogai-core/SKILL.md:2`). Its model: every file has one job. Routing files (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`) say where to go next, workflows give ordered steps, references hold durable facts, templates give output shapes, and scripts run repeatable checks (`SKILL.md:14-24`). The route table at `SKILL.md:38-59` maps 16 intents to endpoints:

- `workflows/`: `route-information`, `write-routing-file`, `write-workflow`, `write-reference`, `write-template`, `write-script`, `write-argc-file`, `audit-framework`, `validate-schema`, `write-hook-tests`.
- `references/`: `at-linking`, `claude-md-routing-rules`, `routing-framework`, `xml-tags`, `naming-and-ownership`.
- `templates/`: `agents-md`, `claude-md`, `routing-file`, `simple-skill`, `reference-endpoint`, `workflow-endpoint`.

Agent-facing bodies use semantic XML sections such as `<objective>` and `<routes>` rather than Markdown headings (`SKILL.md:84-85`).

### Schemas and validation

`skills/skogai-core/schemas/` holds 14 JSON Schema (draft 2020-12) files. `schemas/README.md` maps a document's frontmatter `type` to a schema: `skill`, `router`, `workflow`, `reference`, `template`, `script`, `lesson`, `decision`, `pattern`, `principle` and `list`. Each schema states the required sections, for example `<objective>`, `<steps>` and `<validation>` for a workflow, and `<context>`, `<decision>` and `<rationale>` for a decision. `defs`, `frontmatter` and `document` are shared definitions. A `*.list` file with `type: list` validates as an array of checklist entries.

`scripts/validate-schema.sh [ROOT]` prints a schema overview, then runs `scripts/_validate_file.py <schema_dir> <file>` through `uv run` for each file (`validate-schema.sh:95`). The helper is a uv inline script that declares `jsonschema` and `pyyaml`. The target defaults to the skill's own directory, so the skill validates itself. Exit code 1 means at least one file failed. `scripts/create-gh-issue.sh` opens a GitHub issue through `gh` with `--title`, `--body`, optional `--ref` files and `--dry-run`. `scripts/list-xml-tags.sh` was not read.

### Tests

`tests/` holds two Bats files and a helper (`setup_test_dir`, `assert_success`, `assert_output_equals`, file waits). Both suites test code that is not in the tree:

- `tests/skogai-hooks/log-event.bats:6-7` runs scripts from `plugins/skogai-hooks/hooks/scripts`, with the log directory set through `SKOGAI_HOOKS_LOG_DIR`.
- `tests/skogai-jq/skogai-jq.bats:5` sources `plugins/skogai-jq/scripts/skogai-jq.sh`.

There is no `plugins/` directory. Commits `ca81410` and `bf0a819` (2026-07-30) are titled "remove old hooks".

### The `todo/` backlog

`todo/hooks.json` wires six events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`) to scripts in `todo/hooks/`, each with a 10-second timeout. The directory has scripts for more events than are wired, including `worktree-create.sh`, `teammate-idle.sh` and `task-completed.sh`, plus `lesson_matcher.py`, which loads lessons from `$HOME/.skogai/knowledge/lessons` by default (`todo/AGENTS.md:71`). `todo/hooks/pre-tool-use.sh:55` blocks recursive force-deletes of root-like paths. `todo/scripts/skogai-jq.sh` is the shared JSON helper for hooks. `todo/commands/` has 12 slash-command shims such as `commit`, `plan` and `wrapup`. I read the manifest, `AGENTS.md`, `hooks.json` and file names here, not the script bodies.

## How to use it

As documented in the repo; nothing was run.

- Register the marketplace from a checkout: `/plugin marketplace add .` (`todo2/SKILL.md`), then install `skogai-core` or `skogai-tests`.
- Validate typed documents: `skills/skogai-core/scripts/validate-schema.sh [path]`. Needs `uv` and `python3` (3.11 or later per the helper's header). `CLAUDE.md` says not to commit with failures.
- Tests: `bats tests/**/*.bats`, or `/run-tests [plugin-name]`. As described above, both suites point at missing paths.
- `scripts/claude-code-documentation.sh` writes to `./tmp/docs/claude-code` and needs network access. `.gitignore` lists `/tmp/docs/claude-code`.
- There is no build step, no `mise.toml` and no CI configuration.

## Relations to other SkogAI repos

- [skogai-jq](skogai-jq.md) is now the canonical home of the jq library. Its README and AGENTS.md call `todo/skills/skogai-jq` here retired. The survey notes open PR `skogai/skogai-core#6`, which replaces the copy with a pointer; at this commit the copy is still present. This copy lacks the `agents/`, `schemas/` and `schema-fixtures/` directories that skogai-jq has.
- skogai-jq's `schemas/` shares 11 file names with `skills/skogai-core/schemas/` here; the contents differ. Only this repo has `skill.schema.json`.
- The skill calls itself `skogai-routing`, the name of the separate repos `skogai/skogai-routing` and `skogai2/skogai-routing` in the catalog. `SKOGAI.md` shows a tree rooted at `skogai-routing/`, so the skill appears to have been imported from there. No file here states the direction of that copy.
- `todo/.codex-plugin/plugin.json` gives `https://github.com/skogai/.skogai` as the `dot-core` repository, so `todo/` came from the `.skogai` (dot-skogai) repo.
- [skogai2-marketplace](skogai2-marketplace.md) has a plugin with the same name and a different job. Its `TODO.md` has a checked item "Review `todo/` merge into or add as marketplace plugins", but neither repo names the other.
- Hooks here use `SKOGAI_HOOKS_LOG_DIR` (tests) and `SKOGAI_WORKFLOW_DIR` (`todo/scripts/workflow-memory.sh`, `todo/scripts/context/find-agent-root.sh`). `todo/hooks/user-prompt-submit.sh:36` expects a `skogparse` binary at `$HOME/.local/bin/skogparse`. `todo/skills/skogai-gita` refers to repos under `~/claude/` and `~/.local/src/`.

## Gaps and stale references

- `CLAUDE.md:8-9` describes `plugins/skogai-hooks/` and `plugins/skogai-jq/`. Neither exists. The same paths appear in `tests/AGENTS.md`, `tests/TESTING.md`, `tests/skills/skogai-tests/SKILL.md` and both Bats suites, so the test commands in `CLAUDE.md` (`bats ...`, `shellcheck plugins/skogai-hooks/...`) target missing files.
- `skills/skogai-hook-debugging/SKILL.md` cites `plugins/core/hooks/*.sh` twelve times (lines 85-391). That path does not exist either; the matching scripts are under `todo/hooks/`.
- The marketplace entry `skogai-core` lists two skills, but its source is `./`, the whole repo, which also contains `todo/` and `tests/`.
- `tests/README.md` states "Status: early migration" and lists the suites still to move from `todo/tests/` (`session-start`, `pre-tool-use`, `post-tool-use`, `stop`, `user-prompt-submit`, `worktree`, `workflow-memory`).
- The survey reports that the schema validator fails on content that PR #6 does not touch. I did not run the validator.
- Name mismatches: directory `skogai-core` holds skill `skogai-routing`; directory `skogai-hook-debugging` holds skill `hook-debugger`; the root guidance file is `AGENT.md`, not `AGENTS.md`, so the monorepo's `agents/` cache has no copy for this repo.
- Duplicates: `todo2/scripts/` is an older copy of `skills/skogai-core/scripts/` (`_validate_file.py` differs, `create-gh-issue.sh` is absent), and `todo/skills/skogai-hook-debugging/SKILL.md` is identical to the live one.
- Commit `7fde70c` (2026-07-23) has an assistant's planning sentence as its subject line.
- Not read: the workflow, reference and template bodies under `skills/skogai-core/`, the schema JSON files, `tests/TESTING.md` beyond grep hits, and everything under `todo/skills/skogai-jq/`.
