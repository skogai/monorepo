---
permalink: skogai/skogai
type: router
---

<routes>

- .projects/ - sub-projects; each subdir is treated as its own future repo (own SKOGAI.md router, RESEARCH/QUESTIONS docs)
- @WORKSTATION.md - the main project we are working on - the setup of a newly installed workstation
- @DECISIONS.md - what we have agreed upon and questions answered
- @docs/GLOSSARY.md - the glossary: every named thing in this repo and the files it owns
- CORE.md - the SkogAI control-plane repo (~/core): what part it plays long-run — ticket → isolated, context-seeded, agent-ready session (`repo workon`)
- NOTATION.md - the `$`/`@` notation, the skogcli/skogparse toolchain, config-as-namespace, and the entity-generation (append-only → git) model
- @config/ - tool configs (claude-settings, codex, mcp, litellm, statusline, worktrunk); several symlinked into $HOME
- @scripts/ - argc-based shell helpers and context-generation scripts (read scripts/context/AGENTS.md before editing the emitters); the worktree lifecycle hooks are global skogcli scripts, not files here
- openwiki/ - generated evidence index; optional just-in-time context, source and tests stay authoritative
- tasks/ - gptodo task files, one Markdown file each with frontmatter (symlink to `.skogai/tasks/`); list with `gptodo list`, pick with `gptodo next`
- docs/TASK-WORKFLOW.md - workflow: the order to run `gptodo` commands in, which are verified, and the `wt` / `gptodo` handover
- @.inbox/ - quick-capture dumping ground to process and file later
- tmp/docs/claude-code/ - local copy of the official claude code documentation, start at its OVERVIEW.md. The worktree post-start hook fetches it; if missing, fetch it with `skogcli script run claude-code-documentation tmp/docs/claude-code`. _READ IT_ before answering claude code questions
- @tmp/ - scratch space for this repo's work

</routes>

This is the SkogAI knowledge and routing layer: workstation state, decisions, tooling configuration, and per-project research. The runtime control plane lives separately in `~/core`; this repository supplies its context and operational seams. `CLAUDE.md` @-links this file and `AGENTS.md` is a symlink to it, so everything an agent needs is written here directly.

## Conventions

- `@` routes load into every session; plain paths are read on demand.
- Use `./tmp/` (repo-local) for scratch files, not `/tmp/`. Keeps throwaway output attached to this working directory instead of leaking into the global temp namespace, and survives being found later if a session gets interrupted.
- Treat every `.projects/<name>/` as an independently scoped future repository; follow its local router before changing its research or plans.
- `bin/` wrappers keep a fresh clone usable; `.envrc` appends `./bin` so global installs remain preferred.
- Scripts use `argc` annotations. Worktree lifecycle hooks live in the global `skogcli` scripts (read one with `skogcli script code worktree-post-start`); context generators compose shell emitters rather than one monolithic command.

## Anti-patterns

- Do not put project-specific commands in `~/core`; the control plane only dispatches and prepares work contexts.

## Entry points

- `scripts/context/context.sh` builds legacy gptme context from the composable emitters.
- `scripts/context/build-system-prompt.sh` adapts `gptme.toml` context for Claude-like harnesses.
- `config/claude-statusline.js` renders Claude statusline state.
- `gptodo` is optional for legacy context generation; its absence is rendered in the output rather than treated as a fatal error.
- GitHub automation is `.github/workflows/claude.yml`; it dispatches Claude Code when an issue or review contains `@claude`.

## Agent skills

### Issue tracker

Issues live as GitHub issues in `skogai/skogai`.

### Triage labels

Default vocabulary (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix), applied as GitHub labels.

### Domain docs

Single-context — `docs/GLOSSARY.md`. Decisions are logged in `DECISIONS.md`; there is no `docs/adr/`.

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->
