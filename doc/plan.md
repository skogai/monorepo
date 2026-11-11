# SkogAI mise project plan

Status: proposed working roadmap, 2026-11-11. This replaces the initial setup sequence with the owner's five priorities. ADR 0001 remains the accepted tool-selection decision; implementation choices below are proposals until verified and recorded.

**Goal:** Make this monorepo a repeatable, isolated mise workspace, with accessible documentation, composable environments exposed through MCP, a small reusable SkogAI plugin, and a useful mise ecosystem workflow before marketplace integration.

**Architecture:** mise owns tool installation, task execution and environment composition. The root owns project policy; `mise-plugin` owns only reusable environment and PATH behavior. Establish isolation first, then test each integration inside it.

**Tech stack:** mise, Git, the existing Lua environment plugin, usage and packslip; other tools enter for a demonstrated workflow.

**Spec:** The owner's 2026-11-11 priorities, captured as milestones 1–5 below. Marketplace scope remains open and follows those milestones.

For implementation, work one milestone at a time. Each milestone produces its own reviewable change and evidence; this roadmap does not authorize implementing all milestones in one change.

## Constraints and review focus

- Prefer built-in mise functionality and mise-installable tools before custom tooling, per [ADR 0001](adr/0001-starting-tools.md).
- Keep the shared layout in [AGENTS.md](../AGENTS.md). Record exact commands and failures in `.skogai/tests/`; preserve research as written.
- Configuration/state isolation is the first target. It does not restrict arbitrary processes' filesystem or network access; decide separately if an OS security boundary is required.
- Test inherited environment, parent/global/system config, tool lookup and shared caches, not just the current working directory.
- Test two checkouts, paths containing spaces, submodule invocation and missing prerequisites.
- Check environment precedence, conflicting drop-ins and MCP resource refresh explicitly.
- Keep credentials out of experiment records and use dummy values for environment/MCP tests.
- No root application build, test suite or CI currently exists. Checks below are proposed acceptance experiments, not commands claimed to work today.

## Current baseline: source observations

The root `mise.toml` enables monorepo mode, includes only `mise-plugin` as a config root, requests usage and worktrunk at `latest`, and defines a greeting task writing `/tmp/greeting.txt`. It declares the remote `skogai` plugin but invokes `skogai-develop`, relying on a machine-local development link.

`.miserc.toml` selects `skogai`, enables automatic installation and enables `env_conf_d`; the checkout has no corresponding `mise.skogai.toml`. The plugin submodule returns static example values, derives `SKOGAI_MONOREPO_DIR` from `HOME/Work`, and prepends `HOME/.local/bin`. These are prototype behaviors, not the isolation contract.

The earlier [setup evidence](../.skogai/tests/2026-11-10-setup.md) remains historical machine-specific evidence. The [planning evidence](../.skogai/tests/2026-11-11-mise-plan.md) separates this run's source inspection from CLI checks.

## Milestone 1: isolated mise command runner

**Deliverable:** One documented entry point starts mise against this checkout with its own configuration, data, state, cache and temporary directories. It works before any project mise tasks can run.

**Files:** root `mise.toml`, `.miserc.toml`, `.gitignore`, `README.md`; add `bin/mise-sandbox` only if native invocation cannot provide a usable entry point. Put acceptance records in `.skogai/tests/`.

- [ ] Define the isolation contract: checkout root, selected mise executable/version, trusted config scope, permitted host executables and environment allowlist. Git and the initial mise executable are explicit bootstrap prerequisites.
- [ ] Evaluate native directory overrides before writing a launcher: `MISE_CONFIG_DIR`, `MISE_SYSTEM_CONFIG_DIR`, `MISE_DATA_DIR`, `MISE_STATE_DIR`, `MISE_CACHE_DIR`, `MISE_TMP_DIR`. Set these before starting mise, not inside `[env]`.
- [ ] Establish config-discovery boundaries and account for parent configs, explicit global/system config overrides, inherited `MISE_*`, XDG settings and activated tool paths. Do not assume `monorepo_root` stops every form of discovery.
- [ ] Use ignored checkout-local runtime directories. Remove the mandatory workstation plugin link from the isolated path; make trust explicit and determine the intended auto-install behavior.
- [ ] Replace the greeting-only entry point with the smallest useful task workflow after isolation works. Avoid writing shared `/tmp` outputs.
- [ ] Test with dummy conflicting variables/tasks in temporary parent, global and system fixture configs. Assert those values and task names cannot enter the isolated workspace. Never edit the real host configs to run this experiment.
- [ ] Verify installs, plugin links, cache and trust changes stay in the intended local directories. Verify permitted host dependencies are reported and missing prerequisites produce actionable errors.
- [ ] Repeat from the root, a submodule and a second clean checkout with a space in its path. Compare with ordinary host mise to show that the host's configuration and state are unchanged.
- [ ] Record exact commands and results; add only the verified invocation to README and commit a separate PR.

**Exit gate:** A fresh checkout can list and run its tasks without depending on the owner's mise config, plugins or installed tools beyond the declared bootstrap prerequisites. A second-machine run is required before claiming cross-machine reproducibility.

**Interface for later milestones:** the isolated entry point passes mise arguments through unchanged, including repeated `--env` flags and `mcp`, and keeps diagnostics off MCP stdout.

## Milestone 2: readily available mise documentation

**Deliverable:** Humans and agents can find documentation matched to the tested mise version, including offline access.

**Files:** add `doc/mise.md`; update README and root task declarations; keep downloaded documentation in ignored local storage rather than duplicating upstream content in tracked research.

- [ ] Inventory the installed release's help, upstream documentation/source revision, schemas and any packaged documentation resources. Choose the smallest available retrieval method.
- [ ] Provide a documented fetch/update operation with source revision and a local search/read operation. Proposed task names are `docs:fetch` and `docs:search`; define their exact arguments during this milestone.
- [ ] Index configuration discovery, directory overrides, tasks/usage, environments/drop-ins, MCP, environment plugins and packslip. Link authoritative upstream pages from `doc/mise.md`.
- [ ] Test a cold fetch, a warm offline lookup and an explicit update. Report version mismatch instead of silently treating current online docs as proof for an older binary.
- [ ] Record provenance and results; commit the docs workflow PR.

**Exit gate:** From the isolated workspace, another agent can answer where environments are loaded and how a task argument is declared without relying on conversation history or network availability after the initial fetch.

## Milestone 3: composed environments and MCP

**Deliverable:** Reviewed drop-in profiles produce predictable mise contexts for CLI use and MCP clients.

**Files:** `.miserc.toml`, `mise.toml`, `doc/mise.md`, and environment files at paths verified against the pinned version. Do not prescribe a conf.d layout from analogy alone.

- [ ] Verify exact environment drop-in discovery rules and migration behavior of `env_conf_d` for the selected release. Document scope, sort order and precedence relative to `mise.<env>.toml` and `.local` variants.
- [ ] Create minimal `foo` and `bar` fixtures with distinguishable dummy variables and tasks. Exercise no profile, each profile alone, `--env foo --env bar`, and reversed order.
- [ ] Test the user's proposed `mise --env foo --env bar mcp` through the isolated entry point with an explicit checkout working directory. Verify resources for config, tasks and tools match the CLI composition.
- [ ] Verify an MCP task sees the same profiles and local state as the parent server; check trust refusal and safe-mode behavior with fixtures.
- [ ] Test a drop-in edit while a server is alive and after restart. Document the distinction between startup resource snapshots and freshly executed tasks; do not promise hot reload.
- [ ] Define profile names for real needs only after the fixture passes. Produce a client launch example with absolute executable/checkout paths, ordered profile arguments and documented restart behavior.
- [ ] Keep initial profiles free of secrets: `mise://env` can expose real values. Establish an explicit resource/execution policy before connecting credential-bearing environments.
- [ ] Record results and commit the profile/MCP PR.

**Exit gate:** Two different ordered profile compositions can be launched and independently inspected with expected overrides, no host configuration leakage and no protocol contamination on stdout.

**Boundary:** This composes the mise server's project context. It does not establish that mise dynamically aggregates arbitrary third-party MCP servers; that would need a separate requirement and experiment.

## Milestone 4: smallest useful `skogai/mise-plugin`

**Deliverable:** A reusable environment/PATH plugin with a documented contract, usable locally and installed from Git.

**Files:** `mise-plugin/metadata.lua`, `mise-plugin/hooks/mise_env.lua`, `mise-plugin/hooks/mise_path.lua`, `mise-plugin/README.md`, its existing validation configuration; root integration and submodule pointer in a follow-up PR.

- [ ] Define options for an explicit workspace root and optional executable directories; choose variable names and path resolution rules in a proposed ADR before implementing the contract.
- [ ] Let the root supply checkout-specific information. Remove assumptions that every checkout is `HOME/Work` or that every consumer wants `HOME/.local/bin`.
- [ ] Keep hooks fast and deterministic: return environment/PATH values; no downloads, marketplace operations, prompts or machine configuration writes during environment evaluation.
- [ ] Compare native mise templates/PATH declarations with plugin hooks. Put behavior in the plugin only when reuse across consuming repositories earns that abstraction.
- [ ] Test default/minimal options, explicit roots, spaces, missing paths and repeated evaluation. Ensure repeated activation does not accumulate duplicate PATH entries.
- [ ] Test isolated local development linking and remote installation at an immutable revision in a clean consumer. Check the submodule gitdir-link trap explicitly.
- [ ] Fix the existing lint coverage so a successful run actually examines the intended Lua/workflow files. Record which files and checks ran.
- [ ] Deliver the plugin PR, then the monorepo integration PR referencing a reachable tested commit. Owner merges both; no unpublished submodule pointer.

**Exit gate:** The plugin has a useful environment/PATH contract and installs without the original workstation. Root tasks remain ordinary mise tasks; installing an environment plugin alone is not claimed to distribute task definitions.

## Milestone 5: mise ecosystem workflow

**Deliverable:** One useful workflow demonstrating mise + usage + packslip, with other jdx tools added for specific jobs.

**Files:** root `mise.toml`, verified lockfile if appropriate, README and `doc/mise.md`; existing submodule task config only where it owns the workflow.

- [ ] Inventory candidate tools and their role: mise for orchestration, usage for argument/help/completion definitions, packslip for supported release distribution and verification. Evaluate hk for existing plugin checks and adr-tools for decisions; do not install a whole catalog by default.
- [ ] Resolve bootstrap direction: the initial mise binary must be available before mise installs anything. Evaluate packslip as a bootstrap method separately from mise's packslip backend; avoid a circular prerequisite.
- [ ] Choose one useful task with arguments and help, then run it via CLI and the milestone-3 MCP context. Verify argument handling including spaces and invalid input.
- [ ] Test one supported tool installed through the packslip backend, including version selection, verification behavior and install destination inside isolation. Check available packaged help/completion resources rather than duplicating them.
- [ ] Select version/update policy from these experiments. Pin reproducibility-sensitive versions and test any lockfile on target platforms; record unsupported platforms and network requirements.
- [ ] Make documentation retrieval, task help, plugin validation and ADR discovery a fresh-checkout walkthrough. Resolve the existing ADR 0001 numbering collision without overwriting it when introducing adr-tools.
- [ ] Record results, update README and deliver the workflow PR.

**Exit gate:** A clean checkout can bootstrap the declared prerequisites, retrieve docs and run a real parameterized workflow through CLI and MCP with recorded tool provenance.

## Later: marketplace management

Keep this as a follow-on project, not a prerequisite for milestones 1–5. Which marketplaces and clients to support remains open; the owner has not selected Claude Code, Codex or another ecosystem.

- [ ] Select the first target and define whether management means discovering sources, installing plugins, updating, enabling/disabling or publishing a marketplace.
- [ ] Inspect that client's supported CLI/config interfaces and existing mise package-manager plugins before building an adapter.
- [ ] Keep source registration, installed versions and client activation distinct. Specify project/user scope and an inspectable desired-state format.
- [ ] Prototype status and dry-run first in the isolated environment, then explicit apply, repeatability, update and removal of only owned entries. Preserve unmanaged client configuration.
- [ ] Compare a few ordinary mise tasks with a package-manager plugin; choose the smallest interface that meets the tested need. Keep side effects out of environment hooks.
- [ ] Add a second target only after the first is repeatable. Record lifecycle and compatibility decisions in ADRs.

## Delivery and retained work

Work in milestone order. Each PR identifies the agent, harness, machine, checkout and base commit, includes evidence, and leaves merging to the owner. Failures stay in the evidence; a passing workstation experiment is not a universal guarantee.

The previous plan's Neovim schema support, encryption/bootstrap, T3/herdr/worktrunk workflow, ticket routing and legacy repository naming remain backlog items. They should not delay the first isolated runner. No encryption mechanism, extra task runner, application language or root CI is selected here.

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


## Authoritative references consulted

These are documentation observations, not runtime verification. Recheck them against the version selected in milestone 1.

- [mise directories](https://mise.jdx.dev/directories.html)
- [Configuration and environment files](https://mise.jdx.dev/configuration)
- [MCP interface and refresh behavior](https://mise.jdx.dev/mcp.html)
- [Environment plugins](https://mise.jdx.dev/env-plugin-development.html)
- [Package-manager plugins](https://mise.jdx.dev/bootstrap/packages/plugins.html)
- [packslip backend](https://mise.jdx.dev/dev-tools/backends/packslip.html)
- [Packaged documentation and completions](https://mise.jdx.dev/dev-tools/packslip-resources.html)
