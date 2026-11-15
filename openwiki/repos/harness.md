---
type: repository
title: harness
description: Meta/overview workspace for the SkogAI agent-harness rebuild. It holds harness pattern docs, four earlier hook-framework attempts (three packaged as plugins under marketplace/), validators, schemas and plans; about 85% of the tracked files are vendored or copied material, and the root router file is a dead end.
tags: [harness, claude-code, hooks, plugins, research, work-in-progress]
repo: skogai/harness
commit: 31a54d7
last_commit: 2026-11-09
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/harness/CLAUDE.md
  - repos/harness/SKOGAI.md
  - repos/harness/QUESTIONS.md
  - repos/harness/mise.toml
  - repos/harness/.envrc
  - repos/harness/.gitmodules
  - repos/harness/.gitignore
  - repos/harness/bin/skogcli
  - repos/harness/bin/gptodo
  - repos/harness/prompt-for-claude-code-researcher.md
  - repos/harness/.github/workflows/claude.yml
  - repos/harness/.codex/hooks.json
  - repos/harness/.codex/hooks/_codex-adapter.sh
  - repos/harness/.claude/hooks/README.md
  - repos/harness/.claude/hooks/package.json
  - repos/harness/.claude/scripts/sync-agent-skills.sh
  - repos/harness/.scripts/AGENTS.md
  - repos/harness/.scripts/validate_router.py
  - repos/harness/.scripts/check-skills.sh
  - repos/harness/.skogix/schemas/AGENTS.md
  - repos/harness/.skogix/todo/gsd-planning/PROJECT.md
  - repos/harness/.skogix/todo/gsd-planning/STATE.md
  - repos/harness/.docs/README.md
  - repos/harness/.docs/what-is-a-harness.md
  - repos/harness/.docs/harness/pattern-language.md
  - repos/harness/.docs/archive/README.md
  - repos/harness/.docs/archive/session-handoff.md
  - repos/harness/.docs/harness-engineering/README.md
  - repos/harness/.docs/harness-engineering/package.json
  - repos/harness/.docs/harness-engineering/LICENSE
  - repos/harness/research/hook-framework/README.md
  - repos/harness/research/hook-framework/plan.md
  - repos/harness/research/hook-framework/plugin-engine-audit.md
  - repos/harness/.skogai/plans/crystalline-stirring-harbor.md
  - repos/harness/.omo/plans/skogharness-immediate-next-work.md
  - repos/harness/scripts/match-lessons.py
  - repos/harness/marketplace/SKOGAI.md
  - repos/harness/marketplace/README.md
  - repos/harness/marketplace/.claude-plugin/marketplace.json
  - repos/harness/marketplace/plugins/skogharness/AGENTS.md
  - repos/harness/marketplace/plugins/skogharness/.claude-plugin/plugin.json
  - repos/harness/marketplace/plugins/skogharness/ecc/install-state.json
  - repos/harness/marketplace/plugins/skogharness/hooks/hooks.json
  - repos/harness/marketplace/plugins/skoghooks/SKOGAI.md
  - repos/harness/marketplace/plugins/skoghooks/hooks/hooks.json
  - repos/harness/marketplace/plugins/skogix-hooks/AGENTS.md
  - repos/harness/marketplace/plugins/skogix-hooks/hooks.json
  - repos/harness/marketplace/plugins/skogix-hooks/.codex-plugin/plugin.json
  - repos/harness/marketplace/plugins/skogix-core-original/SKILL.md
  - repos/harness/marketplace/plugins/skogix-core-original/SKOGAI.md
---

# harness

**`skogai/harness` is the meta/overview workspace for rebuilding the SkogAI agent harness: it collects harness design docs, several earlier hook-framework attempts, validators, schemas and plans, but ships no product of its own.** `mise.toml:1-3` says so directly: "This dir is the dev/overview environment, not a shipped artifact — actual products (and their own tests) live one level down, e.g. in marketplace/." State: work in progress, slow. The last four commits (2026-09-24 to 2026-11-09) are titled "WIP" and mostly bump the two submodule pointers; the last substantive content commit is `075fadf` (2026-09-18, research docs and plans). The root instruction file `SKOGAI.md` contains only a route to itself, and `QUESTIONS.md` lists open decisions that are still unanswered.

Of 4,950 tracked files, about 4,220 are vendored or copied material (see "Own work versus vendored" below).

## Source map

| Path | Holds |
|---|---|
| `CLAUDE.md` | Router: frontmatter plus `<routes>` pointing at `@SKOGAI.md`. |
| `SKOGAI.md`, `AGENTS.md` | `AGENTS.md` is a symlink to `SKOGAI.md`. `SKOGAI.md` is a router whose only route is `@SKOGAI.md` (itself). No content. |
| `QUESTIONS.md` | Open questions from a cleanup session, plus an "Already done" list. Partly stale (see Gaps). |
| `mise.toml` | Tool pins (node 26, bun 1.3.14, python 3.14, uv, usage), `.venv` auto-create, optional `.env`, one task `install-skogcli`. |
| `.python-version` | `3.13` (disagrees with `mise.toml`). |
| `.envrc` | Four commented-out lines; no active direnv config. |
| `.gitmodules` | Submodules `skogharness` (skogai/skogharness) and `skills` (skogai/skills). Both directories are empty in the clone. |
| `bin/` | Four one-line wrappers: `skogcli`, `install-skogcli`, `gptodo`, `gita`. |
| `.docs/what-is-a-harness.md`, `.docs/harness/` | Own harness concept doc and pattern language (11 files, about 1,870 lines). |
| `.docs/archive/` | Docs from the previous harness generation (a manifest-driven `skogharness` CLI): specs, features, blueprint, vision, `progress.md`, `session-handoff.md`. |
| `.docs/harness-engineering/` | 2,475 files. Vendored copy of the third-party "Learn Harness Engineering" course (MIT, WalkingLab; VitePress site in 15 languages, six projects, a `harness-creator` skill). |
| `marketplace/` | 2,078 files. A Claude Code marketplace layout with four plugin directories under `plugins/`, payload fixtures, scaffold scripts. |
| `.claude/hooks/` | 60 files. TypeScript/shell skill-activation hook framework (with compiled `.js`, AI provider adapters, committed `state/` files). |
| `.claude/skills/`, `.agents/skills/` | 66 and 65 files. Skill set (superpowers-style skills, backend/frontend dev guidelines, `skill-developer`, `new-hook`) and its mirror for Codex-style agents. |
| `.claude/tests/` | 48 files. Test scripts for a "superpowers" plugin (brainstorm server, opencode, codex, pi). The code they test is not in this repo. |
| `.claude/scripts/` | `sync-agent-skills.sh`, `verify-setup.sh`, `skill-stats.sh`, `index-sessions.ts`. |
| `.codex/` | `hooks.json`, `hooks/_codex-adapter.sh`, `agents/auto-error-resolver.toml`: Codex wiring onto `.claude/hooks/`. |
| `.scripts/` | 24 files. Python/shell validators with unit tests, from the old `skogharness` CLI repo. |
| `.skogix/schemas/` | 19 JSON Schema (Draft 2020-12) files for document types, manifest, agent, messages. |
| `.skogix/todo/gsd-planning/`, `.skogix/.old-planning-example/` | GSD planning workspace for the old CLI (PROJECT, ROADMAP, STATE, codebase map). The two directories are byte-identical. |
| `research/hook-framework/` | Five docs: reference architecture, review of the earlier attempts, fix plan, plugin engine audit. |
| `.skogai/plans/crystalline-stirring-harbor.md` | Plan for a Pydantic schema layer, heavily annotated with rejecting owner comments. |
| `.omo/plans/`, `.omo/drafts/` | One work plan and its draft ("skogharness-immediate-next-work"). |
| `scripts/match-lessons.py` | 1,602-line gptme-style lesson matcher hook for Claude Code. |
| `prompt-for-claude-code-researcher.md` | A request prompt: research how to run Claude Code with a near-empty context. |
| `.github/workflows/claude.yml` | `@claude` mention workflow using `anthropics/claude-code-action@v1`. |
| `tmp/.gitkeep` | Placeholder; `/tmp` is gitignored. |

## How it works

There is no single program. The repo is a collection of parts around one question, stated in `.docs/what-is-a-harness.md`: "what is the harness here, exactly?"

### Own work versus vendored

| Part | Files | Origin |
|---|---|---|
| `.docs/harness-engineering/` | 2,475 | Vendored third-party course. Added in one commit (`404d592`, 2026-09-14). Its `LICENSE` is MIT, copyright WalkingLab. |
| `marketplace/plugins/skogix-hooks/skills/skogai-jq/` | 1,083 | Copy of the SkogAI jq-transforms library (60+ transforms, each a directory with schema and tests). |
| `marketplace/plugins/skogharness/` | 666 | Rebranded install of "Everything Claude Code" (ECC) 2.0.0. `AGENTS.md:1` still reads "Everything Claude Code (ECC) — Agent Instructions"; `ecc/install-state.json` records the install (2026-07-14, profile `developer`) and source paths under a local ECC plugin cache. |
| `.claude/skills/`, `.claude/tests/`, most of `.claude/hooks/` | about 170 | Imported from public skill/hook collections (commits titled "superpowers", "skogharness"); `.claude/hooks/README.md` and `.claude/skills/README.md` are written as a showcase to copy from. |
| `.docs/harness/`, `.docs/what-is-a-harness.md`, `research/`, `QUESTIONS.md`, plans, `.skogix/schemas/`, `.scripts/`, `marketplace/plugins/skoghooks/` hook scripts, `skogix-hooks/hooks/`, `skogix-core-original/` | few hundred | SkogAI-authored. |

### Harness docs (`.docs/`)

`.docs/what-is-a-harness.md` defines a harness as request assembly, turn loop, tool plane, memory plane, transcript/recovery and extension plane, and routes into `.docs/harness/`. `.docs/harness/pattern-language.md:17-28` indexes ten patterns by plane and links the deep-dive files (context engineering, tool registry, memory persistence, lifecycle bootstrap, skill runtime, multi-agent, modular automation), plus `principles.md` and `gotchas.md`. `.docs/README.md` states these were moved here from `.skogix/` "during the knowledge-extraction stage".

`.docs/archive/` describes the previous generation: a Node/Bun `skogharness` CLI driven by a `skogai.json` manifest with `init`, `sync`, `status`, `add` and `harness-init` commands. None of that source (`src/`, `bin/cli.js`, `test/`, `package.json`) is in this repo.

### The hook-framework attempts

`research/hook-framework/plan.md:5-11` names four independent attempts, all present in the tree:

1. **`.claude/hooks/`** — skill auto-activation. `skill-activation-prompt` (UserPromptSubmit) reads `.claude/skills/skill-rules.json` and injects skill suggestions; `skill-verification-guard` (PreToolUse), `post-tool-use-tracker` (PostToolUse) and `session-doc-updater` (Stop) complete the set. TypeScript run through `tsx`, with `lib/` (embeddings, vector store, session state) and `providers/` (Gemini, OpenAI, Anthropic, Ollama). No `.claude/settings.json` exists, so Claude Code does not load these from this repo. `.codex/hooks.json` wires the same four scripts for Codex through `.codex/hooks/_codex-adapter.sh`, which sets `CLAUDE_PROJECT_DIR` and splits an `apply_patch` payload into one synthetic `Edit` event per file (`_codex-adapter.sh:28-52`).
2. **`marketplace/plugins/skogharness/`** — the ECC install: 67 agent definitions, 92 commands, 80 skills under `skills/skogai/`, 122 rule files under `rules/skogai/`, and a Node hook runtime in `scripts/hooks/` and `scripts/lib/`. `hooks/hooks.json` (354 lines) registers PreToolUse, PreCompact, SessionStart, PostToolUse, PostToolUseFailure, Stop and SessionEnd. `.claude-plugin/plugin.json` declares only `skills` and `commands`; `PLUGIN_SCHEMA_NOTES.md` documents manifest constraints.
3. **`marketplace/plugins/skoghooks/`** — one Python script per lifecycle event (13 events), each a PEP 723 `uv run` script. `hooks/hooks.json:48-188` wires them with `${CLAUDE_PLUGIN_ROOT}` paths. Hooks log JSONL to a per-session runtime directory and exit 0 unless deliberately blocking. Its `scripts/hooks/` and `scripts/lib/` (144 files) are a second copy of the ECC Node runtime from attempt 2.
4. **`marketplace/plugins/skogix-hooks/`** — shell hook routers plus `hooks/lesson_matcher.py`. Its manifest is `.codex-plugin/plugin.json` and names the plugin `dot-core` 0.0.4 with repository `skogai/.skogai`; `AGENTS.md` is titled "dot-core plugin". `hooks.json` wires six events (SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop) while `hooks/` holds 19 shell scripts. Bats tests are under `tests/`. Skills: `skogai-jq`, `skogai-gita`, `skogai-hook-debugging`, `skogdocs`, `skogai-worktrunk`.

`research/hook-framework/plugin-engine-audit.md` (2026-09-16) concludes that none of the plugins provides one stable hook engine and that the reusable base is small: host-native loading, one payload fixture per event, tests that execute the exact registered command, an append-only JSONL writer, and one consistency check. `research/hook-framework/README.md` names `skogix-hooks` as the first target.

### Marketplace wrapper (`marketplace/`)

`marketplace/.claude-plugin/marketplace.json` defines a marketplace named `skoghooks` with a single plugin, `./plugins/skoghooks`. The other three plugin directories are not listed. `marketplace/SKOGAI.md` (its `CLAUDE.md` routes there, `AGENTS.md` symlinks to it) documents the skoghooks layout, the hook pattern and flags. `marketplace/scripts/new_hook.py` scaffolds a hook from `marketplace/templates/hook_template.py`; `marketplace/scripts/test_hooks.py` pipes `marketplace/tests/payloads/<Event>.json` (14 fixtures) through the commands wired in `hooks.json`. `marketplace/.claude/.codebase-info/` is a generated codebase map (9 files); `marketplace/.todo/` holds six memory-style notes.

`marketplace/plugins/skogix-core-original/` is a copy of the `skogai-routing` skill: `SKILL.md` (name `skogai-routing`), `workflows/`, `references/`, `templates/`, `schemas/` (14 files) and `scripts/`. It has no plugin manifest.

### Validators and schemas

`.skogix/schemas/` layers `defs`, `frontmatter` and `document` schemas under per-type schemas (router, workflow, reference, template, script, lesson, pattern, decision, principle, skill) and data shapes (manifest, agent, list, message, skogchat-message, transform). `.scripts/validate-schema.sh` calls `.scripts/_validate_file.py`, which maps a document's `type` to a schema (`_validate_file.py:30`). `.scripts/validate_router.py:34` reads `.skogix/schemas/router.schema.json`. Other validators check skill quality, skill language, skill closure, reference neutrality, profile consistency and plugin metadata; most have a `test_*.py` beside them.

### Lesson matching

`scripts/match-lessons.py` is a Claude Code hook for UserPromptSubmit and PreToolUse. It finds the workspace root by looking for `gptme.toml`, reads lesson directories from its `[lessons] dirs`, matches keywords against the prompt, tool input and recent transcript, and injects matches as `additionalContext`, tracking already-injected lessons per session. `skogix-hooks/hooks/lesson_matcher.py` and `skoghooks/hooks/lesson_matcher.py` are separate, smaller matchers; the former loads lessons from `$HOME/.skogai/knowledge/lessons` by default (`skogix-hooks/AGENTS.md`).

### Not read

- `.docs/harness-engineering/`: only `README.md`, `package.json`, `LICENSE` and the directory listing.
- `marketplace/plugins/skogharness/`: only `AGENTS.md` (head), manifests, `ecc/install-state.json` (head), `hooks.json` event names and listings. No agent, command, skill, rule or script body.
- `skogai-jq` transforms, `.claude/tests/`, `.claude/skills/` bodies, the TypeScript in `.claude/hooks/`, the individual `skoghooks` and `skogix-hooks` hook scripts, Bats tests, most of `.docs/archive/`, `.skogix/todo/` beyond PROJECT and STATE, `research/hook-framework/attempts-review.md` and `reference-architecture.md`, and the bodies of the `.scripts/` validators.
- The two submodules: not initialised in the clone, so their content is unknown here.

## How to use it

Nothing was run for this page; the commands below are as the repo's files state them.

- Environment: `mise trust && mise install` (`mise.toml:5-6`). Machine settings and secrets (`SKOGAI_MODE`, `SKOGAI_GH_TOKEN`) belong in `~/.config/mise/config.toml`, `.env` or `mise.local.toml`, not in the repo (`mise.toml:8-10`).
- `mise run install-skogcli` runs `uv tool install git+https://github.com/skogai/cli`. `bin/skogcli` runs the same CLI through `uv tool run` after setting `SKOGAI_CONFIG_DIR=.skogai/config/<repo name>`; it needs `gh` and `jq`.
- `bin/gptodo` runs gptodo from `gptme/gptme-contrib` through `uv tool run`; `bin/gita` runs `gita`.
- Submodules: `git submodule update --init` is needed to populate `skogharness/` and `skills/`.
- skoghooks plugin, from `marketplace/` (`marketplace/SKOGAI.md`): `claude --plugin-dir ./plugins/skoghooks` to test locally; `/plugin marketplace add ./` then `/plugin install skoghooks@skoghooks`; `uv run scripts/new_hook.py <Event> <name>`; `uv run scripts/test_hooks.py`; `claude plugin validate ./plugins/skoghooks`. Requires `uv`; `user_prompt_submit.py --name-agent` optionally uses local Ollama (`OLLAMA_MODEL`).
- skogix-hooks, from its directory (`skogix-hooks/AGENTS.md`): `bats tests/*`, `uvx pytest hooks/test_lesson_matcher.py -v`. Uses `SKOGAI_WORKFLOW_DIR`.
- Skill mirror: `.claude/scripts/sync-agent-skills.sh [--check]` copies `.claude/skills/*` to `.agents/skills/`.
- `.claude/hooks/`: `npm install` in that directory; optional AI mode reads `SKILL_AI_PROVIDER`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (`.claude/hooks/.env.example`).
- CI: `.github/workflows/claude.yml` needs the secret `CLAUDE_CODE_OAUTH_TOKEN`.

There is no root test or check task; they were removed deliberately (`QUESTIONS.md`, "Already done").

## Relations to other SkogAI repos

- `skogai/skogharness` and `skogai/skills`: git submodules at `skogharness/` and `skills/` (`.gitmodules`). Neither is in the monorepo catalog (`mani.yaml`). `.skogai/plans/crystalline-stirring-harbor.md` describes `skogharness` as "the new, currently empty repo" where the next generation is to be built.
- `skogai-routing` (in catalog; `skogai2-skogai-routing` is cloned): `marketplace/plugins/skogix-core-original/` is a copy of it, and `.skogix/schemas/` plus `.scripts/validate-schema.sh`, `_validate_file.py`, `list-xml-tags.sh` are a larger variant of its `schemas/` and `scripts/`.
- `skogai-jq` (in catalog): copied in full at `marketplace/plugins/skogix-hooks/skills/skogai-jq/`.
- `dot-skogai` (`skogai/.skogai`): `skogix-hooks` is the `dot-core` plugin from that repo, by its own manifest and `AGENTS.md`. `.docs/archive/session-handoff.md` says `.skogai` in the old checkout was a symlink into a separate `dot-skogai` git repo.
- `skogai/cli` (`skogai2-cli` in catalog): installed by `mise.toml` and `bin/install-skogcli`, run by `bin/skogcli`.
- Shared conventions: router files with `type: router` frontmatter and a `<routes>` block of `@path` bullets; `AGENTS.md` as a symlink to `SKOGAI.md`; `permalink:` frontmatter; `.skogai/` as a state directory.
- External: gptme (`scripts/match-lessons.py`, `bin/gptodo`), Everything Claude Code, the WalkingLab course, worktrunk.

## Gaps and stale references

- `SKOGAI.md` routes only to itself, so `CLAUDE.md` and `AGENTS.md` both resolve to a file with no content. `QUESTIONS.md` item 2 describes an earlier version of the same dead end (an empty bullet); commit `d1a48d5` changed it to the self-reference.
- `QUESTIONS.md` item 1 is still open: `router.schema.json` expects `description` and `routing` sections, while every real router uses a plain `<routes>` list, so `validate_router.py` is reported to fail on them.
- `QUESTIONS.md` says `.claude/settings.bare.json` was created. Commit `5e5f413` (2026-09-16) later deleted it together with `.claude/settings.json`, commands and agents. No settings file is tracked under root `.claude/`.
- `research/hook-framework/plugin-engine-audit.md` states the `.claude/hooks` attempt "was removed in commit `5e5f413`". The directory is still tracked (60 files); that commit removed settings, commands and agents, which unwired the hooks.
- `research/hook-framework/plan.md` refers to "this repo" as the sound-notification reference repo and to this repo as `/home/skogix/.local/src/harness1`; the docs were written elsewhere and copied in.
- `.scripts/AGENTS.md` and `.skogix/schemas/AGENTS.md` describe `scripts/`, `schemas/`, `../src-js/manifest.js`, `../test/install-global-script.test.js` and `bun run test`. The directories are now `.scripts/` and `.skogix/schemas/`; `src-js/`, `test/` and a root `package.json` do not exist.
- `.scripts/check-skills.sh:8` checks `.claude/skills`; other `.scripts/` validators target a CLI source tree that is not here.
- `.omo/plans/skogharness-immediate-next-work.md` audits staged changes to `Argcfile.sh`, `bin/all`, `functions.json` and `argc build`; none of those exist in this repo. `.skogix/todo/gsd-planning/STATE.md` is at phase 1 of 5, 0%, last updated 2026-07-08, and plans the removed CLI.
- `.skogix/.old-planning-example/` duplicates `.skogix/todo/gsd-planning/` exactly. `.docs/README.md` mentions `.skogix/skills/`, which does not exist.
- `marketplace/README.md` and the marketplace description still advertise TTS alerts and `rm -rf`/`.env` blocking; `marketplace/SKOGAI.md` says there is no TTS and that the blocking checks are disabled.
- Three of the four plugin directories are not in `marketplace.json`. `skogharness` carries its own nested `.claude-plugin/marketplace.json`; `skogix-hooks` has only a Codex manifest; `skogix-core-original` has none.
- The ECC Node runtime is duplicated: `scripts/hooks/` (48 files) and `scripts/lib/` (96 files) are identical in `skogharness` and `skoghooks`.
- Hard-coded machine paths: `skogix-hooks/skills/skogai-worktrunk` is a symlink to an absolute path under `/home/skogix/.local/src/worktrunk/`, broken on any other machine; `skogharness/ecc/install-state.json` and the `.skogix` planning intel files embed `/home/skogix/...` paths.
- `.claude/hooks/state/` (session docs, `metrics.jsonl`) is runtime state committed to git. `.claude/skills` and `.agents/skills` have drifted in three skills, and `.agents/skills/source-command-verify-setup` has no source in `.claude/skills`.
- `.python-version` (3.13) and `mise.toml` (python 3.14) disagree.
- `.skogai/plans/crystalline-stirring-harbor.md` is a plan the owner rejected inline; it is not a description of work done.
