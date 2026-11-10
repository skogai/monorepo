# SkogAI 3.0: first working plan

Status: proposed execution plan, 2026-11-10.

## Starting point

This is the first official setup-documentation session. The aim is to explain and test the setup already being assembled, then grow it through small, recorded experiments.

Read all 21 workspace files discovered outside Git internals, including the three research notes, the personal todo, root configuration, and the plugin source, types, and CI configuration. This inventory covers this checkout, not home-directory configuration or remote repositories.

The parent README identifies this as `skogai/monorepo`. It currently composes three Git submodules: `skogai`, `skogix`, and `mise-plugin`. Both identity repositories have placeholder READMEs. Their historical roles still need the owner's explanation.

Mise declares the monorepo root and discovers `mise-plugin` as a config root. The root activates `skogai-develop`, while the declared remote plugin is named `skogai`. A comment describes the development name as a local plugin link; its reconstruction is not documented yet. The plugin derives the workspace as `$HOME/Work`, so cloning elsewhere is an explicit portability test. Most tools use `latest`.

## Decisions and research

The [starting-tool ADR](adr/0001-starting-tools.md) records the choices named in the [original todo](../skogix/.skogai/todo.list): mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations.

The research is input, not an adopted specification:

- [Claude](../.skogai/research/monorepo-claude.md) surveys monorepo, documentation, retrieval, and tracking options.
- [Codex](../.skogai/research/monorepo-codex.md) proposes Markdown, GitHub workflow, and a fresh-clone smoke test.
- [Gemini](../.skogai/research/monorepo-gemini.md) proposes a larger directory layout and service/tool stack.

Carry forward the useful principles: searchable Markdown, explicit decisions, small changes, and repeatable setup checks. Defer Taskfile, language workspaces, databases, RAG, a docs website, and a ticket-system choice until an actual need is recorded. Research claims about adoption and existing infrastructure have not been independently verified here; they do not establish what this machine runs.

## 1. Record the baseline

- Keep `doc/` for durable documentation and `doc/adr/` for decisions, matching the todo's spelling.
- Use root `.skogai/research/` for research; propose `.skogai/tests/` for small experiment records when needed. Keep personal planning in `skogix/.skogai/` for now.
- Record which configuration comes from the checkout and which comes from the workstation.
- Describe `skogai/monorepo`, `skogai/skogai`, `skogai/skogix`, and `skogai/mise-plugin`, including legacy names and whether submodules are a lasting choice or a transition.

Done when a new session can find the plan, decisions, known checks, and unresolved questions from the README.

## 2. Make the mise experiment repeatable

- Document development-plugin installation/linking and remote-plugin usage separately.
- Exercise `hello` with a known argument; check its output and documented `/tmp/greeting.txt` side effect.
- Verify environment and PATH hooks from the root and plugin directory.
- Establish a lint invocation that actually checks all intended files; record tool versions and results.
- Try a recursive clone in a temporary location and record every required external prerequisite, trust step, and local configuration dependency.
- Decide how to handle `$HOME/Work` and version pinning based on those results.

Done when another checkout can repeat the checks using the written instructions. A successful test on this workstation alone is insufficient.

## 3. Exercise one real workflow

- Document how the owner starts work in T3 Code and what role herdr serves.
- Take one small documentation change through the chosen branch, review, and completion process.
- Record what the human decides, what the agent does, and where results are stored.
- If messaging is part of that workflow, explicitly test delivery and reply separately. No messaging test has run in this session.

Done when one real change has a traceable request, diff, verification result, and completion record. Choose issue/PR automation only as this workflow calls for it.

## 4. Finish the remaining setup experiments

- Neovim schemas: demonstrate mise completion and a diagnostic for one intentionally invalid example.
- `.skogai` layout: record scope and ownership of root versus personal files before adding more directories.
- Encryption/bootstrap: choose the mechanism in an ADR, then demonstrate an encrypted dummy-value round trip and bootstrap recovery. Record key prerequisites without storing secrets in the experiment log.

Done when each experiment has a command or procedure, expected result, actual result, and decision or next action.

## Session evidence: 2026-11-10

- `git status --short`: clean before documentation changes.
- `git submodule status`: all three submodules initialized at recorded commits; no mismatch markers.
- `mise --version`: `2026.11.5 linux-x64 (2026-11-09)`.
- `mise tasks --all`: finds `//:hello`, `//mise-plugin:lint`, and `//mise-plugin:lint-fix`. Also lists `bootstrap`, absent from workspace files; its source remains to be identified.
- `mise plugins ls`: includes `skogai` and `skogai-develop`; listing alone does not prove their provenance.
- `mise exec -- sh` assertions: `SKOGAI_ENV_VAR`, `SKOGAI_MONOREPO_DIR`, and `SKOGAI_CONFIG_DIR` match the plugin implementation. PASS on this workstation.
- `mise run //mise-plugin:lint`: exits 0, but reports zero modified files and `hk no files to run`. Full lint remains unverified.
- Fresh-clone bootstrap, greeting task, PATH behavior, CI, editor schemas, encryption, and cross-session messaging: not tested.

For the next experiment, append: date, question, prerequisites, exact command, expected result, actual result, and resulting decision. Preserve failures as evidence.

## Owner context still needed

The role of herdr, the meaning of legacy repository names, the intended long-term submodule arrangement, and tests/decisions made before this checkout's notes. Add these when available; do not infer them from the research proposals.
