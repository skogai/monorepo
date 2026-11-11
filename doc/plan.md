# SkogAI 3.0: first setup plan

Status: working plan, 2026-11-10. Merged on 2026-11-11 from pull requests 1, 3, and 2/4 (2 and 4 are the same commit).

Goal: document the setup already in use, test it in small steps, and let the results decide the next changes. A working fresh-checkout recipe is the first milestone.

## Starting point

The [backlog](../skogix/.skogai/todo.list) names mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations as the starting tools. [ADR 0001](adr/0001-starting-tools.md) records that choice.

The repository is a root plus three Git submodules: `skogai`, `skogix`, and `mise-plugin`. The root mise config enables monorepo mode and lists only `mise-plugin` as a config root. The plugin supplies environment variables and a PATH entry. `skogai` holds a README; `skogix` holds a README and the backlog.

Work here is done by several agents in parallel on different machines. [AGENTS.md](../AGENTS.md) sets the rules that follow from that. Everything tested so far is in the [setup evidence](../.skogai/tests/2026-11-10-setup.md), with each result attributed to the run that produced it.

## How to use the research

The [Claude survey](../.skogai/research/monorepo-claude.md), [Codex defaults](../.skogai/research/monorepo-codex.md), and [Gemini proposal](../.skogai/research/monorepo-gemini.md) are inputs. Their external statistics have not been reverified, and their claims about existing Python, database, or Notion usage are not established by this repository.

All three agree on Markdown in Git and on text search with `rg` or `git grep` before any retrieval layer. The Claude survey and the Gemini proposal name decision records. The Codex defaults and the Gemini proposal ask for a fresh-clone README. Only the Codex defaults propose one small end-to-end workflow test. This plan carries all five forward as its own choices.

The owner's rule, recorded in ADR 0001, is to use mise as much as possible: a tool mise can install is free to use and comes before any tooling of our own. Defer the rest until a recorded need appears, each with its own ADR:

- A second task runner or build orchestrator (Taskfile, Turborepo, Nx, Moon). mise monorepo tasks already cover this and were seen working.
- A language workspace (uv, pnpm), Postgres with pgvector, Docker Compose, and a docs site.
- The `apps/`, `packages/`, `mcps/` directory tree. Submodules are the unit for now.

## Open questions for the owner

- Tickets: GitHub Issues, the backlog file, or the backlog as inbox with an item becoming an Issue once it needs a pull request.
- Which parts of the global and system mise configuration belong in the repository or the plugin, and which are workstation prerequisites.
- Whether `SKOGAI_MONOREPO_DIR` should identify the checkout or a fixed home directory.
- herdr's role, and how T3 Code, herdr, and worktrunk fit together.
- What `.miserc.toml` is for. It selects a `skogai` mise environment, but the repository has no `mise.skogai.toml`.
- What the legacy SkogAI repositories and names map to, and whether submodules are a lasting choice or a transition.

## Steps

Each step is small, ends in a commit, and is done when another session on another machine can follow its instructions and reproduce the result.

### 0. Hygiene

- Restore a `.gitignore`. The one removed in `6d0ce28` ignored `/SECRETSINHERE/` and `/.qmd`.
- Keep `AGENTS.md` current as the rules change.

Check: `git status --short` prints nothing in a clean checkout.

### 1. Record the baseline

- Keep durable documentation in `doc/` and decisions in `doc/adr/`, matching the backlog's spelling.
- Add `adr-tools` to `mise.toml` and manage decision records with it. Settle the numbering clash with the existing ADR 0001 when running `adr init`.
- Turn each answered open question into an ADR.
- Describe `skogai/monorepo`, `skogai/skogai`, `skogai/skogix`, and `skogai/mise-plugin`, including legacy names.
- Define what a `.skogai/` directory holds at each level. Root holds shared context; a submodule's holds context specific to it.

Check: `rg -n --hidden 'Starting tools' doc` finds ADR 0001.

### 2. Make the mise setup repeatable

- Document how the `skogai-develop` plugin link is created, separately from using the remote `skogai` plugin. The submodule's relative `gitdir: ../.git/modules/mise-plugin` is a known trap when the link is made by hand.
- Explain `.miserc.toml`: which files `env = ["skogai"]` and `env_conf_d = true` load on a fresh clone, and what `auto_install = true` installs without asking.
- List which starting tools come from operating system packages instead of mise, per machine.
- Run `mise run hello skogai` and check the output and the `/tmp/greeting.txt` side effect.
- Verify the environment and PATH hooks from the root and from `mise-plugin`.
- Establish a lint invocation that checks all intended files. The current one exits 0 having checked none.
- Resolve the global-versus-repository environment collisions listed in the evidence.
- Clone recursively into a temporary location and record every prerequisite, trust step, and missing bootstrap step.
- Decide on `SKOGAI_MONOREPO_DIR` and on which tool versions to pin instead of `latest`.
- Write the verified bootstrap steps into the README.

Check: the same commands give the same results in a second checkout on a second machine.

### 3. Exercise one real workflow

- Document how the owner starts work in T3 Code and what herdr and worktrunk do.
- Take one small documentation change from request through branch, edit, validation, review, and completion. Record what the human decides, what the agent does, and where results are stored.
- If messaging between sessions is part of the workflow, test delivery and reply separately and record both. No messaging test has run.
- Try a pull request and CI round trip only once that workflow is chosen.

Check: one change has a traceable request, diff, verification result, and completion record.

### 4. Finish the remaining setup experiments

- Neovim schemas: show mise completion and a diagnostic for one deliberately invalid example.
- Encryption and bootstrap: choose the mechanism in an ADR, then show a round trip with a dummy secret and a bootstrap recovery. One workstation's `mise doctor` reports a dotfiles problem that blocks this path.
- Search: `rg` is the baseline. Trial qmd over `doc/` and `.skogai/` only if a need appears, and decide in an ADR.

Check: each experiment has a command, an expected result, an actual result, and a decision or next action in `.skogai/tests/`.

## First milestone

A new checkout can initialize the submodules, establish the documented mise plugin setup, run the greeting and plugin checks, and find the starting-tools decision with text search. One T3-driven change has a recorded validation and review outcome. Every machine-specific prerequisite is written down.
