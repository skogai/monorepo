---
title: SKOGAI
permalink: dot-skogai/skogai
type: router
---

<MEGADUMP>
<DUMP>

<routes>

- @bin/ - executables, `$PATH`-style, no file extension
- `./docs/[$project]/` - a folder with documentation for each [$project]
- `./references/` -> `dot-skogai/docs/[$project]` - a dynamic/project specific symlink to the projects documentation
- @SKOGIX.md - the users own routing file
- @knowledge/SKOGAI.md
- @memory/SKOGAI.md
- @docs/SKOGAI.md
- @agents/SKOGAI.md - self-contained agent bundles
- @scripts/SKOGAI.md - shared automation, integrations, validators
- @projects/SKOGAI.md - small project-specific workspaces and research

- @knowledge/SKOGAI.md
- @memory/SKOGAI.md
- @docs/CLAUDE.md
- @personal/skogix/SKOGIX.md - the users routing file

```filetree
.
|- Argcfile.sh       # root command router
|- argc/             # language runners, declaration generation, MCP bridge/server
|- agents/           # self-contained agent bundles
|- tools/            # callable tool implementations
|- bin/              # generated executable shims; do not hand-author
|- scripts/          # shared automation, integrations, validators
|- docs/             # upstream reference material and local operational docs
|- knowledge/        # durable decisions, lessons, reusable patterns
|- memory/           # curated working context and feedback
|- projects/         # small project-specific workspaces and research
`- tools.txt, agents.txt, functions.json, mcp.json  # generated/runtime registries
```

</routes>

<modules>

SkogAI is a script-first workspace for agent bundles, callable tools, MCP plumbing, durable knowledge, and operational documentation. `argc` is the root command framework; this is intentionally not a conventional application tree.

## skogai-lessons

hooks inject `lesson_matcher.py` loads lessons `knowledge/lessons/` at session startup and then pattern match the messages for things like matching keywords depending on tool used, statistics and so on. then it scores each matched lesson against the current hook mode (`session-start`, `prompt`, `tool`) and injects top-scoring lessons into `additionalcontext`. always exits 0 (fail-open). yaml parsing falls back to a regex parser if `pyyaml` is unavailable.

## skogai-jq

the skill `/skogai-jq` holds 70+ composable json transforms. each transform is a self-contained directory:

```filetree
crud-get/
├── transform.jq      # pure jq, 5–40 lines
├── schema.json       # input/output/args contract
├── test.sh           # 8–17 tests minimum
└── test-input-*.json # per-test fixtures
```

all transforms receive json on stdin, take parameters via `--arg`/`--argjson`, and chain via unix pipes. have a lot of references for things like use cases or jq pitfalls (especially `try-catch` vs `//` and `has()` vs `!= null`).

## skogai-workflow

a plugin which focus on creating persistent state via writing to files `task_plan.md`, `findings.md`, `progress.md` that live in the project working directory. its hooks inject plan context at `userpromptsubmit` and `pretooluse`, and nudge completion at `stop`.

</modules>

<knowledge>

information which have stood the test of time and proven itself as worth knowing in the long term. things worth sharing with everyone in skogai no matter context, circumstances and are seen as a global truth for everyone involved.

| store     | location               | purpose                                               |
| --------- | ---------------------- | ----------------------------------------------------- |
| lessons   | `knowledge/lessons/`   | injected by lesson_matcher; yaml frontmatter required |
| decisions | `knowledge/decisions/` | adr-style, date-prefixed filenames                    |
| patterns  | `knowledge/patterns/`  | timeless patterns, no date prefix                     |

<decisions>

- @knowledge/DECISIONS.md - contains routing information with a brief description of each decision and where to find more information about it
- @templates/ contains a templates for creating decisions, lessons and create workflows for patters

</decisions>

<lessons>

- @knowledge/lessons/CLAUDE.md
  lessons use keyword-based auto-loading: include `match.keywords` in yaml frontmatter so `skogai-lessons` can surface them contextually.
  minimum required frontmatter:

```yaml
---
match:
  keywords: [keyword1, keyword2]
status: active # active | automated | deprecated | archived
version: 1 # increment on meaningful rewrites
---
```

the matcher loads all lessons at session start, scores each against the current message/tool context, and injects top-scoring lessons into `additionalcontext`. always exits 0 (fail-open).

</lessons>

<patterns>

patterns reusable solutions which are used over and over - creating a workflow of using similar solutions over and over again.  
use when a recurring problem has a well-understood solution worth capturing independent of any specific decision or incident.
minimum required frontmatter:

```yaml
---
type: pattern
tags: [tag1, tag2]
---
```

</patterns>

</knowledge>

<memory>
used for basic and direct information gathering. temporary context needed for short term memory, gathering information and to see direct connections between concepts. a memory file or folder should be written to at least once every three turns if a healthy workflow is followed.

| store  | location          | purpose                                                            |
| ------ | ----------------- | ------------------------------------------------------------------ |
| memory | @memory/          | working context which focus on updating a little bit very often    |
| memory | @memory/CLAUDE.md | routing index: questions, projects, glossary, feedback, references |

</memory>

<hooks>

hooks are the primary mechanism for context injection, pipeline control and in general the most important part of any harness. programmatic tools to help, remind and push the context where we want claude to end up, to find or take into consideration.  
they fire at specific points in the agents lifecycle, each with a defined payload shape and blocking behavior.

| hook               | blocking     | primary use                                   |
| ------------------ | ------------ | --------------------------------------------- |
| `UserPromptSubmit` | no           | inject context, load lessons, patch prompt    |
| `PreToolUse`       | yes (exit 2) | validate or block tool calls before execution |
| `PostToolUse`      | no           | log results, update session state             |
| `Stop`             | no           | nudge completion, write summary               |

- every basic workflow-hook follows the same steps:

1. reads a json payload from stdin
2. logs / appends the event to `/tmp/<session_id>.jsonl`
3. sets up the needed environment with skogai-jq, helpers and loaders
4. with a single invocation per step/row a script may take a single string as input and return an exit code and the new prompt which gets sent to the next in line
   - example: `lesson_matcher.py` reads the message sent, pattern matches against frontmatter and injects relevant lessons by appending them to the message prompt
5. outputs a json payload containing the modified message

</hooks>

<conventions>

- hook entrypoints are thin routers; shared logic or bigger modules belong in `scripts/`.
- lesson, concept and other docs require yaml frontmatter. keep injected/router files concise.
- session state flows through `/tmp/<session_id>.jsonl` — treat as ephemeral.
- Keep router and hook entrypoints thin; shared logic belongs in `scripts/`.
- Shell surfaces use Bash, `set -e`, argc annotations, and `eval "$(argc --argc-eval "$0" "$@")"`.
- Tools and agents are manifest-driven: update `tools.txt` or `agents.txt`, then generate declarations and shims through `argc`.
- JS tools/agents use CommonJS exports and JSDoc schemas; MCP packages use ESM. Python is script-first with per-file metadata, not a root package.
- Use `@` references for current repository context; preserve YAML frontmatter where a content type requires it.

</conventions>

<rules>

- no `src/` tree, no makefile, no `.eslintrc`/`pyproject.toml`/`package.json` at root unless a genuine new boundary requires it.
- do not add backwards-compat shims or scaffolding that crosses the dot-core / skogai-workflow / workstation boundary.
- Do not hand-edit generated `bin/` shims or `functions.json`; regenerate them through `argc`.
- Do not hardcode `/home/skogix/...`, commit `.env`, use `git add .`, or hide errors and warnings.
- Do not use the deprecated `scripts/context/tasks.py`; use `gptodo`.

</rules>

<commands>

```bash
argc check
argc build
argc test
argc run@tool <tool> '<json>'
argc run@agent <agent> <action> '<json>'
argc mcp check
```

</commands>

<notes>

- No root CI workflow, formatter, or conventional unit-test suite exists; validation is script- and demo-driven.
- `argc test` exercises demo tools and agents; use `argc check` for dependencies and environment checks.
- Scoped rules live in child `SKOGAI.md`/`CLAUDE.md` files where a domain has distinct constraints. Existing `CLAUDE.md` and `SKOGAI.md` files remain authoritative routers for their domains.

</notes>

</DUMP>
</MEGADUMP>

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->
